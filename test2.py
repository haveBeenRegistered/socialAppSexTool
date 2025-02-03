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

# 查找并聚焦到搜索框
try:
    search_box = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, 'js-header-search-form-v2--keyword'))
    )
    driver.execute_script(
        "arguments[0].focus();", search_box)  # 使用 JavaScript 聚焦
    search_box.click()  # 点击进入输入框
    search_box.send_keys('React.js')
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

# 查找并点击类名为 MuiButtonBase-root 且 data-value 为 new 的按钮
try:
    new_value_button = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[contains(@class, "MuiButtonBase-root") and @data-value="new"]'))
    )
    new_value_button.click()
except Exception as e:
    print(f'Element with data-value "new" not found: {e}')


# 等待排序结果加载
time.sleep(2)

# 查找类名为 MuiBox-root css-hn63dx 的公司的元素，并点击第一个
try:
    elements = WebDriverWait(driver, 2).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, '//*[contains(@class, "MuiBox-root") and contains(@class, "css-hn63dx")]'))
    )
    if elements:
        elements[0].click()
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

    else:
        print('No elements found with class name "MuiBox-root css-hn63dx"')
except Exception as e:
    print(
        f'Error finding elements with class name "MuiBox-root css-hn63dx": {e}')

# 等待操作完成
time.sleep(2)


try:
    apply_buttons = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, '//*[contains(@class, "measurement-click-job-apply-button")]'))
    )
    if apply_buttons:
        apply_buttons[0].click()
    else:
        print('No apply buttons found')
except Exception as e:
    print(f'Error finding or clicking the apply button: {e}')
# 等待操作完成
time.sleep(1)

try:
    meeting_buttons = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, '//*[contains(@class, "MuiFormControlLabel-labelPlacementEnd")]'))
    )
    if len(meeting_buttons) >= 4:
        meeting_buttons[3].click()  # 点击第四个按钮（索引从0开始）
        print('Fourth apply button clicked')
    else:
        print('Less than 4 apply buttons found')
except Exception as e:
    print(f'Error finding or clicking the apply button: {e}')

time.sleep(1)

try:
    meeting_buttons = WebDriverWait(driver, 2).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, '//*[contains(@class, "MuiButton-outlinedSizeSmall")]'))
    )
    if len(meeting_buttons) >= 2:
        meeting_buttons[0].click()  # 点击第四个按钮（索引从0开始）
        print('Fourth apply button clicked')
    else:
        print('Less than 4 apply buttons found')
except Exception as e:
    print(f'Error finding or clicking the apply button: {e}')

# 等待操作完成
time.sleep(1)

try:
    # 查找文本输入框并赋值
    text_area = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located(
            (By.XPATH, '//textarea[@id="job-apply-message"]'))
    )
    text_area.send_keys(
        "Reactをメインのフレームワークとするプロジェクト開発に引き続き参加したいと強く思っています。\n以前作成したReact.jsとNext.jsのブランチを連携いたします。\nhttps://bitbucket.org/havebeenregistered/master/branch/master")
    print('Text area value set')
except Exception as e:
    print(f'Error finding or setting value to the text area: {e}')
time.sleep(1)

try:
    # 等待并查找目标按钮
    meeting_button = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[contains(@class, "MuiButton-outlinedSizeSmall")]'))
    )
    if meeting_button:
        meeting_button.click()  # 点击找到的按钮
        print('Button clicked')
    else:

        print('No buttons found')
except Exception as e:
    print(f'Error finding or clicking the button: {e}')

time.sleep(1)

try:
    # 使用 PyAutoGUI 输入文件路径并确认
    file_path1 = r"C:\Users\81804\Desktop\転職資料\400\転職用業務経歴書_陳傑.pdf"
    file_path2 = r"C:\Users\81804\Desktop\転職資料\400\履歴書_陳傑.pdf"
    # 连接到文件上传对话框
    app = Application().connect(title_re="打开", class_name="#32770")
    dialog = app.window(title_re="打开")

    # 输入文件路径
    dialog.Edit.type_keys(file_path1, with_spaces=True)
    time.sleep(1)
    dialog.Button.click()
    dialog.Button.click()
    time.sleep(1)

    # 等待并查找目标按钮
    meeting_button = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[contains(@class, "MuiButton-outlinedSizeSmall")]'))
    )
    if meeting_button:
        meeting_button.click()  # 点击找到的按钮
        # 等待文件上传对话框打开
    time.sleep(1)
    # 连接到文件上传对话框
    app = Application().connect(title_re="打开", class_name="#32770")
    dialog = app.window(title_re="打开")
    # 输入文件路径
    dialog.Edit.type_keys(file_path2, with_spaces=True)
    time.sleep(1)
    dialog.Button.click()
    dialog.Button.click()
    time.sleep(1)

    print('File uploaded')
except Exception as e:
    print(f'Error finding or uploading the file: {e}')
time.sleep(1)
try:
    # 找到弹出表单的元素
    form_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            # 替换为实际的表单类名或ID
            (By.XPATH, '//*[contains(@class, "MuiDialog-paperScrollPaper")]'))
    )

    # 将表单的滚动条移动到底部
    driver.execute_script(
        "arguments[0].scrollTop = arguments[0].scrollHeight;", form_element)
    time.sleep(1)  # 等待滚动完成
    post_buttons = WebDriverWait(driver, 2).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, '//*[contains(@class, "measurement-post-job-apply-button")]'))
    )
    if post_buttons:
        post_buttons[0].click()  # 点击找到的第一个按钮
        print('Button clicked')
    else:
        print('No apply buttons found')

except Exception as e:
    print(f'Error finding or clicking the apply button: {e}')

# 等待操作完成
time.sleep(1)

# 切换回最先的页面
try:
    original_window = driver.window_handles[0]
    driver.switch_to.window(original_window)
    print('Switched back to the original window')
except Exception as e:
    print(f'Error switching back to the original window: {e}')

# 查找类名为 MuiBox-root css-hn63dx 的公司的元素，并点击第一个
try:
    elements = WebDriverWait(driver, 2).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, '//*[contains(@class, "MuiBox-root") and contains(@class, "css-hn63dx")]'))
    )
    if elements:
        elements[1].click()
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

    else:
        print('No elements found with class name "MuiBox-root css-hn63dx"')
except Exception as e:
    print(
        f'Error finding elements with class name "MuiBox-root css-hn63dx": {e}')

# 等待操作完成
time.sleep(2)

# 执行操作
perform_actions(driver)


# 打印页面标题
print(driver.title)

# 暂停以查看结果

input("Press Enter to continue...")

# 关闭浏览器
driver.quit()
