# test4.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pyautogui
import subprocess
from pywinauto import Application
from loop import perform_actions  # 导入 perform_actions 函数
import os


def upload_file(file_path):
    try:
        # 连接到文件上传对话框
        app = Application().connect(title_re="打开", class_name="#32770")
        dialog = app.window(title_re="打开")

        # 输入文件路径
        dialog.Edit.type_keys(file_path, with_spaces=True)
        time.sleep(1)
        dialog.Button.click()
        dialog.Button.click()
        time.sleep(10)

        print(f'File {file_path} uploaded')
    except Exception as e:
        print(f'Error finding or uploading the file {file_path}: {e}')


# 配置 WebDriver 路径
# 请将此路径替换为你的 ChromeDriver 路径
driver_path = 'C:/driver/chromedriver-win64/chromedriver.exe'
# 创建 ChromeDriver 服务
service = Service(driver_path)

# 启动 Chrome 浏览器并启用远程调试
# 请将此路径替换为你的 Chrome 可执行文件路径
chrome_executable_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
subprocess.Popen([chrome_executable_path,
                 '--remote-debugging-port=9222', '--user-data-dir=C:/ChromeDebug'])
time.sleep(2)  # 等待浏览器启动
# 最大化浏览器窗口
pyautogui.hotkey('alt', 'space')
time.sleep(1)
pyautogui.press('x')
time.sleep(1)


pyautogui.hotkey('enter')
time.sleep(1)
# 模拟键盘输入网址并回车
url = 'https://drive.google.com/drive/home'
pyautogui.typewrite(url)
time.sleep(2)
pyautogui.hotkey('enter')  # 使用 press 方法模拟按下回车键
pyautogui.hotkey('enter')

# 等待页面加载
time.sleep(2)  # 根据网络情况调整等待时间

# 配置 ChromeOptions 以连接到远程调试端口
options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

# 启动 ChromeDriver 并连接到远程调试端口
driver = webdriver.Chrome(service=service, options=options)

try:
    # 等待并查找目标按钮
    meeting_button = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[contains(@class, "brbsPe Ss7qXc a-qb-d")]'))
    )
    if meeting_button:
        meeting_button.click()  # 点击找到的按钮
        meeting_button.click()
        print('Button clicked')
    else:
        print('No buttons found')
except Exception as e:
    print(f'Error finding or clicking the button: {e}')

time.sleep(2)

try:
    # 等待并查找目标按钮
    up_buttons = WebDriverWait(driver, 2).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, '//*[contains(@class, "h-v")]'))
    )
    if len(up_buttons) >= 2:
        up_buttons[14].click()  # 点击找到的第二个按钮（索引从0开始）
        print('Second button clicked')
    else:
        print('Less than 2 buttons found')
except Exception as e:
    print(f'Error finding or clicking the button: {e}')

time.sleep(1)

try:
    # 上传第一个文件
    file_path1 = os.path.join("C:\\", "Users", "81804", "Desktop", "転職資料", "400", "転職用業務経歴書_陳傑.pdf")
    upload_file(file_path1)

    print('Files uploaded')
except Exception as e:
    print(f'Error finding or uploading the file: {e}')
time.sleep(3)
try:
    # 等待并查找目标按钮
    meeting_button = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[contains(@class, "brbsPe Ss7qXc a-qb-d")]'))
    )
    if meeting_button:
        meeting_button.click()  # 点击找到的按钮
        print('Button clicked')
    else:
        print('No buttons found')
except Exception as e:
    print(f'Error finding or clicking the button: {e}')

time.sleep(2)

try:
    # 等待并查找目标按钮
    up_buttons = WebDriverWait(driver, 2).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, '//*[contains(@class, "h-v")]'))
    )
    if len(up_buttons) >= 2:
        up_buttons[14].click()  # 点击找到的第二个按钮（索引从0开始）
        print('Second button clicked')
    else:
        print('Less than 2 buttons found')
except Exception as e:
    print(f'Error finding or clicking the button: {e}')

time.sleep(1)

try:
    # 上传第一个文件
    file_path2 = os.path.join("C:\\", "Users", "81804", "Desktop", "転職資料", "400", "履歴書_陳傑.pdf")
    upload_file(file_path2)

    print('Files uploaded')
except Exception as e:
    print(f'Error finding or uploading the file: {e}')
time.sleep(3)
