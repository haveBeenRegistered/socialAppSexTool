from pywinauto.application import Application
import pyautogui
import time
import pyperclip
import re

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

def input_chinese_text(text):
    """
    输入中文文本
    :param text: 要输入的中文文本
    """
    try:
        # 将中文文本复制到剪贴板
        pyperclip.copy(text)
        time.sleep(0.5)
        
        # 使用快捷键粘贴
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)
        return True
    except Exception as e:
        print(f"中文文本输入失败: {e}")
        return False
    
def process_wechat_message(search_text):
    """
    处理微信消息发送流程
    :param search_text: 搜索文本
    """
    # 点击聊天
    move_and_click([15, 91, 47, 123])  # 需要调整坐标

    # 点击搜索框
    move_and_click([86, 23, 232, 46])  # 需要调整坐标

    # 输入搜索文本
    input_chinese_text(search_text)
    time.sleep(1)

    # 点击聊天框 BoundingRectangle	[l=54,t=60,r=279,b=90]
    move_and_click([54, 60, 279, 150])  # 需要调整坐标
    
    # 点击输入文本框
    move_and_click([385, 918, 1912, 994])  # 需要调整坐标

    with open("message.txt", "r", encoding="utf-8") as f:
        content = f.read()
    
    # 提取 message= 后的内容，不要求必须有引号
    match = re.search(r'message\s*=\s*"?([^"\n]+)"?', content)
    if match:
        message_content = match.group(1)
    else:
        raise Exception("message.txt 中未找到 message 信息")
    # 使用函数输入文本
    input_chinese_text(message_content)
    # 发送消息file
    pyautogui.press('enter')
    time.sleep(1)

# 启动微信应用程序
# app = Application(backend='uia').start(r"D:\WeChat\WeChat.exe")
# 从 message.txt 中读取路径
with open("message.txt", "r", encoding="utf-8") as f:
    content = f.read()
    match = re.search(r'path\s*=\s*"?([^"\s]+)"?', content)
if match:
    exe_path = match.group(1)
else:
    raise Exception("message.txt 中未找到 path 信息")
app = Application(backend='uia').start(exe_path)

# 等待应用程序完全加载
time.sleep(5)

# 最大化窗口
move_and_click([1259, 195, 1292, 220])  # 需要调整坐标

# 读取文件并循环处理
lines = []
with open('wechatSex.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

for i, line in enumerate(lines):
    search_text = line.strip()  # 去除换行符
    if search_text == "":  # 如果是空字符串File
        print("武运昌隆")
        exit()  # 结束程序
    process_wechat_message(search_text)
    time.sleep(2)  # 每次处理后等待
    
    # 如果是最后一行
    if i == len(lines) - 1:
        print("武运昌隆")
        exit()  # 结束程序