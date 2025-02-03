# test3.py
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
url = 'https://www.green-japan.com/'
pyautogui.typewrite(url, interval=0.1)
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

# 查找并聚焦到搜索框
try:
    search_box = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located( 
            (By.CLASS_NAME, 'js-header-search-form-v2--keyword'))
    )
    driver.execute_script(
        "arguments[0].focus();", search_box)  # 使用 JavaScript 聚焦ｘ
    search_box.click()  # 点击进入输入框
    search_box.send_keys('Angular')  # 输入搜索关键字
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)  # 根据网络情况调整等待时间
except Exception as e:
    print(f'Error finding or interacting with the search box: {e}')

# 查找并点击指定的按钮
try:
    initial_button = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[contains(@class, "MuiSelect-select") and contains(@class, "MuiSelect-outlined") and contains(@class, "MuiInputBase-input") and contains(@class, "MuiOutlinedInput-input") and contains(@class, "MuiInputBase-inputSizeSmall") and contains(@class, "css-4toe3a")]'))
    )
    initial_button.click()
except Exception as e:
    print(f"Initial button not found: {e}")

# 查找并点击类名为 MuiButtonBase-root 且 data-value 为 new 的按钮 更新顺序
try:
    new_value_button = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[contains(@class, "MuiButtonBase-root") and @data-value="new"]'))
    )
    new_value_button.click()
except Exception as e:
    print(f'Element with data-value "new" not found: {e}')

# 默认顺序
# try:
#     new_value_button = WebDriverWait(driver, 2).until(
#         EC.element_to_be_clickable(
#             (By.XPATH, '//*[contains(@class, "MuiButtonBase-root") and @data-value="jobOfferScore"]'))
#     )
#     new_value_button.click()
# except Exception as e:
#     print(f'Element with data-value "new" not found: {e}')


# 等待排序结果加载
time.sleep(2)


def click_and_perform_actions(driver, max_iterations):
    for index in range(max_iterations):
        try:
            elements = WebDriverWait(driver, 2).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '//*[contains(@class, "MuiBox-root") and contains(@class, "css-hn63dx")]'))
            )
            if elements and len(elements) > index:
                elements[index].click()
                time.sleep(2)
                # 打印所有窗口句柄
                print(f'Window handles: {driver.window_handles}')

                # 切换到新窗口
                driver.switch_to.window(driver.window_handles[-1])
                print('Switched to new window')

                # 等待新页面加载完成
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'body')))
                print('New page loaded')

                # 执行操作
                perform_actions(driver)

                # 切换回最先的页面
                original_window = driver.window_handles[0]
                driver.switch_to.window(original_window)
                print('Switched back to the original window')
            else:
                print(
                    f'No elements found with class name "MuiBox-root css-hn63dx" at index {index}')
                break
        except Exception as e:
            print(
                f'Error finding elements with class name "MuiBox-root css-hn63dx" at index {index}: {e}')
            break


# 循环二十次
click_and_perform_actions(driver, 40)


# 关闭浏览器
driver.quit()

