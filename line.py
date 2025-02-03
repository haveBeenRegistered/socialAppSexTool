from pywinauto.application import Application
import pyautogui
import time
import pyperclip


def move_and_click(coordinates):
    """
    移动到指定坐标并点击
    :param coordinates: 包含左上右下坐标的数组 [l,t,r,b]
    """
    try:
        # 计算中心点坐标
        x = (coordinates[0] + coordinates[2]) // 2
        y = (coordinates[1] + coordinates[3]) // 2
        
        # 移动鼠标到指定位置
        pyautogui.moveTo(x, y)
        time.sleep(1)  # 等待鼠标移动完成
        
        # 执行点击事件
        pyautogui.click()
        time.sleep(1)
        return True
    except Exception as e:
        print(f"移动点击失败: {e}")
        return False

def input_japanese_text(text):
    """
    输入日语文本
    :param text: 要输入的日语文本
    """
    try:
        # 将日语文本复制到剪贴板
        pyperclip.copy(text)
        time.sleep(0.5)
        
        # 使用快捷键粘贴
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)
        return True
    except Exception as e:
        print(f"日语文本输入失败: {e}")
        return False
    
def process_line_message(search_text):
    """
    处理LINE消息发送流程
    :param search_text: 搜索文本
    """
    # 点击トーク
    move_and_click([15, 91, 47, 123])

    # 点击搜索框
    move_and_click([74, 63, 328, 101])

    # 输入搜索文本
    input_japanese_text(search_text)
    time.sleep(1)

    # 点击聊天框
    move_and_click([62, 131, 374, 202])
    
    # 点击输入文本
    move_and_click([385, 918, 1912, 994])

    # 使用函数输入日语文本
    input_japanese_text('おはよう')

    # 发送消息
    pyautogui.press('enter')
    time.sleep(1)
   

# 启动 LINE 应用程序
app = Application(backend='uia').start(r"C:\Users\81804\AppData\Local\LINE\bin\LineLauncher.exe")

# 等待应用程序完全加载
time.sleep(5)

# 最大化窗口
move_and_click([1864, 11, 1888, 35])

# 读取文件并循环处理
lines = []
with open('lineSex.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

for i, line in enumerate(lines):
    search_text = line.strip()  # 去除换行符
    if search_text == "":  # 如果是空字符串
        print("武运昌隆")
        exit()  # 结束程序
    process_line_message(search_text)
    time.sleep(2)  # 每次处理后等待
    
    # 如果是最后一行
    if i == len(lines) - 1:
        print("武运昌隆")
        exit()  # 结束程序