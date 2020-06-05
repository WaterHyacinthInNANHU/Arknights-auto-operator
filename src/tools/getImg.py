import pyautogui as auto
import keyboard

# im1 = auto.screenshot(region=(0,0, 300, 400))
# im1.save(r"hh.jpg")
#readme:
#此程序用于截取按键图片，使用步骤：
#输入文件路径和名字
#鼠标移动到目标区域左上角
#按空格
#鼠标移动到目标区域右下角
#按空格，完成截图
name = input("input name:")
loc = r"..\\imgs\\"+name+".jpg"
print("loc="+loc)
keyboard.wait(' ')
pos1 = auto.position()
print("get 1/2")
print(pos1)
keyboard.wait(' ')
pos2 = auto.position()
print("get 2/2")
print(pos2)
auto.screenshot(region=(pos1.x,pos1.y, pos2.x-pos1.x, pos2.y-pos1.y)).save(loc)
