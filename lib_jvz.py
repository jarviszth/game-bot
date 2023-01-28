import numpy as np
import cv2 as cv
from time import sleep
import win32gui, win32ui, win32con, win32api, pygetwindow, pytesseract

class JVZ_AI:
    w = 0   
    h = 0
    hwnd = None
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0

    def __init__(self, window_name, size_w, size_h):
        fix = pygetwindow.getWindowsWithTitle(window_name)[0]
        fix.size = (size_w, size_h)
        self.hwnd = win32gui.FindWindow(None, window_name)
        self.hwnd = win32gui.FindWindowEx(self.hwnd, None, None, None)
        if not self.hwnd:
            raise Exception('Window not found: {}'.format(window_name))

        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect[0] - 0
        self.h = window_rect[3] - window_rect[1] - 0

        border_pixels = 0
        titlebar_pixels = 0
        self.w = self.w - (border_pixels * 2)
        self.h = self.h - titlebar_pixels - border_pixels
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels

        self.offset_x = window_rect[0] + self.cropped_x
        self.offset_y = window_rect[1] + self.cropped_y
        
        self.border = 10
        self.titlebar = 36

    def get_screenshot(self):
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)

        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)

        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        img = img[...,:3]
        img = np.ascontiguousarray(img)

        return img
    
    def get_imagepositon(self, needle_img_path, haystack_img, threshold, region = [0, 0, 0, 0], debug_mode = None):
        needle_img = cv.imread(needle_img_path)
        locations = []

        needle_w = needle_img.shape[1]
        needle_h = needle_img.shape[0]
        screen_gray = cv.cvtColor(haystack_img, cv.COLOR_BGR2GRAY)
        image_gray = cv.cvtColor(needle_img, cv.COLOR_BGR2GRAY)
        result = cv.matchTemplate(screen_gray, image_gray, cv.TM_CCOEFF_NORMED)

        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))
        
        rectangles = []
        x1,y1,x2,y2 = region
        for loc in locations:
            if region != [0, 0, 0, 0]:
                if loc[0] >= (x1 - self.border) and loc[1] >= (y1 - self.titlebar) and loc[0] <= (x2 - self.border) and loc[1] <= (y2 - self.titlebar):
                    rect = [int(loc[0]), int(loc[1]), needle_w, needle_h]
                    rectangles.append(rect)
                    rectangles.append(rect)
            else:
                rect = [int(loc[0]), int(loc[1]), needle_w, needle_h]
                rectangles.append(rect)
                rectangles.append(rect)

        # print(rectangles)
        points = []
        if len(rectangles):
            # print('Found needle.')

            line_color = (0, 0, 255)
            line_type = cv.LINE_4
            marker_color = (0, 0, 255)
            marker_type = cv.MARKER_CROSS

            for (x, y, w, h) in rectangles:
                center_x = x + int(w/2)
                center_y = y + int(h/2)
                points.append((center_x, center_y))
                if debug_mode == 'rectangles':
                    top_left = (x, y)
                    bottom_right = (x + w, y + h)
                    cv.rectangle(haystack_img, top_left, bottom_right, color=line_color, lineType=line_type, thickness=1)
                elif debug_mode == 'points':
                    cv.drawMarker(haystack_img, (center_x, center_y), color=marker_color, markerType=marker_type, markerSize=20, thickness=2)
        return points
    
    def get_image2num(self, screen, x1, y1, x2, y2):
        image = screen[(y1 - self.titlebar):(y2 - self.titlebar),(x1 - self.border):(x2 - self.border)]
        w = image.shape[1]
        h = image.shape[0]
        img = np.array(image)
        img = cv.resize(img,(w*2, h*2))
        img = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
        getNum = str(pytesseract.image_to_string(img,config='--psm 6 -c tessedit_char_whitelist="0123456789/"'))
        return getNum
    
    def get_image2bitmap(self, screen, RGB, region = [0,0,0,0]):
        screen = np.array(screen)
        screen = cv.cvtColor(screen,cv.COLOR_BGR2RGB)
        
        if region != [0,0,0,0]:
            x0,y0,x1,y1 = region
            screen = screen[(y0 - self.titlebar):(y1 - self.titlebar),(x0 - self.border):(x1 - self.border)]

        RGB = np.array(RGB)
        result = cv.inRange(screen,RGB,RGB)
        
        for XY in np.transpose(result.nonzero()):
            if len(XY) != 0:
                return True
        else:
            return False
    
    def click(self, position, delay = 0):
        x, y = position[0]
        mouse = win32api.MAKELONG(x, y)
        win32gui.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, mouse)
        win32gui.SendMessage(self.hwnd, win32con.WM_LBUTTONUP, None, mouse)
        sleep(delay)