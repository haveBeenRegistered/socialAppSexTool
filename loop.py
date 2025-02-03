from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from pywinauto import Application
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


def perform_actions(driver):
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
            meeting_buttons[0].click()  # 点击第一个按钮
            print('First apply button clicked')
        else:
            print('Less than 2 apply buttons found')
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
        # text_area.send_keys(
        #     "貴社ますますご清栄のこととお喜び申し上げます。Reactをメインのフレームワークとするプロジェクト開発に引き続き参加したいと強く思っています。\n以前作成したReact.jsとNext.jsのブランチを連携いたします。\nhttps://bitbucket.org/havebeenregistered/master/branch/master\nまた、ウェブサイトドメインも併せてご覧ください。\nhttps://checkoutreact.top/#/qrlogin?mobile=13211111111&code=246810\n何卒よろしくお願い申し上げます。")
        text_area.send_keys(
            "貴社ますますご清栄のこととお喜び申し上げます。\n以前作成したReact.jsとNext.jsのブランチを連携いたします。\nhttps://bitbucket.org/havebeenregistered/master/branch/master\nまた、ウェブサイトドメインも併せてご覧ください。\nhttps://checkoutreact.top/#/qrlogin?mobile=13211111111&code=246810\n何卒よろしくお願い申し上げます。")
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
        # 上传第一个文件
        file_path1 = os.path.join("C:\\", "Users", "81804", "Desktop", "転職資料", "400", "転職用業務経歴書_陳傑.pdf")
        upload_file(file_path1)

        # 找到弹出表单的元素
        form_element = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[contains(@class, "MuiDialog-paperScrollPaper")]'))
        )

        # 选中表单元素
        form_element.click()
        time.sleep(1)

        # 将表单的滚动条移动到底部
        driver.execute_script(
            "arguments[0].scrollTop = arguments[0].scrollHeight;", form_element)
        time.sleep(1)  # 等待滚动完成

        meeting_button.click()  # 点击找到的按钮
        # 等待文件上传对话框打开
        time.sleep(1)

        # 上传第二个文件
        file_path2 = os.path.join("C:\\", "Users", "81804", "Desktop", "転職資料", "400", "履歴書_陳傑.pdf")
        upload_file(file_path2)

        print('Files uploaded')
    except Exception as e:
        print(f'Error finding or uploading the file: {e}')
    time.sleep(3)
    try:

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
