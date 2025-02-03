from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# 配置 WebDriver 路径
driver_path = 'C:/driver/chromedriver-win64/chromedriver.exe'  # 请将此路径替换为你的 ChromeDriver 路径
# 创建 ChromeDriver 服务
service = Service(driver_path)

# 启动 Chrome 浏览器
driver = webdriver.Chrome(service=service)

# 打开一个测试网页
driver.get('https://www.google.com')

# 打印页面标题
print(driver.title)

# 关闭浏览器
driver.quit()