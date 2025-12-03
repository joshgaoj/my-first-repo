from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# 配置Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 无头模式，隐藏浏览器窗口
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 目标URL
login_url = 'https://member.rakuten-sec.co.jp/app/info_jp_prc_stock.do'

# 打开登录页面
driver.get(login_url)

# 等待页面加载（可根据实际情况调整）
time.sleep(5)

# 输入用户名和密码
username = driver.find_element(By.ID, 'QPVX7849')  # 根据实际的用户名输入框ID
password = driver.find_element(By.ID, 'dnc.2009')  # 根据实际的密码输入框ID
username.send_keys('QPVX7849')  # 替换为实际的用户名
password.send_keys('dnc.2009')  # 替换为实际的密码

# 提交表单
password.send_keys(Keys.RETURN)

# 等待登录完成（可根据实际情况调整）
time.sleep(5)

# 访问目标页面
driver.get('https://member.rakuten-sec.co.jp/app/info_jp_prc_stock.do?eventType=init&infoInit=1&contentId=2&type=null&sub_type=null&local=null&dscrCd=13430&marketCd=1&gmn=J&smn=01&lmn=01&fmn=01')

# 等待页面加载
time.sleep(5)

# 获取页面内容
html = driver.page_source

# 使用BeautifulSoup解析HTML内容
soup = BeautifulSoup(html, 'html.parser')
table = soup.find('table', class_='tbl-data-01')

if table:
    rows = table.find_all('tr')
    table_data = []
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        table_data.append([ele for ele in cols if ele])
    for row in table_data:
        print(row)
else:
    print('未找到 class 为 "tbl-data-01" 的表格')

# 关闭浏览器
driver.quit()
