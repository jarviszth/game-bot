import pytesseract, cv2
import numpy as np

image = cv2.imread('9.png')
w = image.shape[1]
h = image.shape[0]
img = np.array(image)
img = cv2.resize(img,(w*2, h*2))
img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
getNum = str(pytesseract.image_to_string(img,config='--psm 6 -c tessedit_char_whitelist="0123456789/"'))
print(getNum)