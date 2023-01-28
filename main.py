import cv2 as cv2
from threading import Thread
from lib_jvz import JVZ_AI

emulator = JVZ_AI('LDPlayer', 1280, 720)
image_path = 'images/'

runquest = False
def coc_quest(screen):
    global runquest
    
    find_carnival = emulator.get_imagepositon(image_path + 'quest_carnival.png', screen, 0.7, region = [819,34,895,110], debug_mode = 'rectangles')
    find_menu = emulator.get_imagepositon(image_path + 'quest_menu.png', screen, 0.7, region = [970,38,1036,104], debug_mode = 'rectangles')
    find_btn_coc = emulator.get_imagepositon(image_path + 'quest_btn_coc.png', screen, 0.7, region = [113,246,245,378], debug_mode = 'rectangles')
    find_go_coc = emulator.get_imagepositon(image_path + 'quest_go_coc.png', screen, 0.7, region = [536,582,705,637], debug_mode = 'rectangles')
    find_coc_mission = emulator.get_imagepositon(image_path + 'quest_coc_ms.png', screen, 0.7, region = [925,482,1196,542], debug_mode = 'rectangles')
    find_coc_accept = emulator.get_imagepositon(image_path + 'quest_coc_accept.png', screen, 0.7, region = [828,567,1021,629], debug_mode = 'rectangles')
    find_coc_cancle = emulator.get_imagepositon(image_path + 'quest_coc_cancle.png', screen, 0.7, region = [830,572,1021,628], debug_mode = 'rectangles')
    find_coc_menu_close = emulator.get_imagepositon(image_path + 'quest_coc_cancle.png', screen, 0.7, region = [1160,37,1234,111], debug_mode = 'rectangles')
    find_coc_give = emulator.get_imagepositon(image_path + 'quest_coc_give.png', screen, 0.7, region = [939,355,1185,410], debug_mode = 'rectangles')
    find_coc_view_npc = emulator.get_imagepositon(image_path + 'quest_coc_view_npc.png', screen, 0.7, region = [868,574,1097,658], debug_mode = 'rectangles')
    find_coc_popup_npc = emulator.get_imagepositon(image_path + 'quest_coc_popup_view_npc.png', screen, 0.7, region = [479,182,622,230], debug_mode = 'rectangles')
    find_coc_store = emulator.get_imagepositon(image_path + 'quest_coc_store.png', screen, 0.7, region = [845,71,1036,122], debug_mode = 'rectangles')
    find_coc_confirm = emulator.get_imagepositon(image_path + 'quest_coc_confirm.png', screen, 0.7, region = [915,462,997,544], debug_mode = 'rectangles')
    find_coc_tab = emulator.get_imagepositon(image_path + 'quest_coc_tab.png', screen, 0.7, region = [67,221,268,451], debug_mode = 'rectangles')
    find_coc_send = emulator.get_imagepositon(image_path + 'quest_coc_send.png', screen, 0.7, region = [889,589,1078,647], debug_mode = 'rectangles')
    
    if not find_carnival and not find_coc_tab:
        if find_menu:
            emulator.click(find_menu, 1)
    
    if find_carnival and not runquest:
        emulator.click(find_carnival, 1)
        runquest = True
        
    if find_btn_coc:
        emulator.click(find_btn_coc, 1)
        
    if find_go_coc:
        emulator.click(find_go_coc, 1)
        
    if find_coc_mission and not find_coc_give:
        emulator.click(find_coc_mission, 1)
        
    if find_coc_accept:
        emulator.click(find_coc_accept, 1)
        
    if find_coc_cancle:
        if find_coc_menu_close:
            emulator.click(find_coc_menu_close, 1)
            
    if find_coc_give:
        emulator.click(find_coc_give, 1)
            
    if not find_coc_popup_npc and find_coc_view_npc:
        emulator.click(find_coc_view_npc, 1)
        
    if find_coc_popup_npc:
        emulator.click([(630, 288)], 1)
        
    if find_coc_store and not find_coc_confirm:
        emulator.click([(540, 480)], 1)
        
    if find_coc_confirm:
        emulator.click([(878, 323)], 1)
        emulator.click([(942, 393)], 1)
        emulator.click(find_coc_confirm, 1)
        emulator.click([(582, 576)], 1)
        emulator.click([(1154, 56)], 1)
        runquest = False
        
    if not runquest and find_coc_tab:
        emulator.click(find_coc_tab, 1)
        
    if find_coc_send:
        emulator.click(find_coc_send, 1)
        runquest = False

fishing_status = False
def fishing(screen):
    global fishing_status
    fishing = emulator.get_imagepositon(image_path + 'fishing.png', screen, 0.7, region = [986,570,1117,619], debug_mode = 'rectangles')
    if fishing and not fishing_status:
        emulator.click([(1027, 504)])
        print('Fishing...')
        fishing_status = True
        
    if fishing_status:
        # gotcha = emulator.get_image2bitmap(screen, (205, 248, 116), region = [982,474,1114,606])
        gotcha = emulator.get_image2bitmap(screen, (176, 235, 96), region = [982,474,1114,606])
        if gotcha:
            emulator.click([(1027, 504)], 1)
            print('Gotcha ><')
            fishing_status = False
   
def Main():
    while True:
        screen = emulator.get_screenshot()
        fishing(screen)
        # coc_quest(screen)
        
        # cv2.imshow("SCREEN MONITOR [Press Q to Exit]", screen)
        # if cv2.waitKey(1) == ord("q"):
        #     cv2.destroyAllWindows()
        #     break
    
if __name__ == "__main__":
    thread = Thread(target = Main)
    thread.start()
    thread.join()