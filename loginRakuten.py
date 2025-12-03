import requests
from bs4 import BeautifulSoup

# 设置登录的URL和目标页面的URL
login_url = "https://member.rakuten-sec.co.jp/app/home.do"
target_url = "https://member.rakuten-sec.co.jp/your_target_page"  # 替换为实际的目标页面URL

# 创建一个会话对象
session = requests.Session()

# 获取登录页面以提取CSRF令牌
response = session.get(login_url)
soup = BeautifulSoup(response.text, 'html.parser')

# 假设CSRF令牌在一个名为_csrf_token的隐藏字段中
csrf_token = soup.find('input', {'name': '_csrf_token'})['value']

# 准备登录数据
login_data = {
    'username': 'QPVX7849',  # 替换为你的用户名
    'password': 'dnc.2009',  # 替换为你的密码
    '_csrf_token': csrf_token,    # 添加CSRF令牌
    # 根据登录页面的表单字段名称替换
    'other_form_fields': 'loginform'
}

# 设置请求头（模拟浏览器）
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': login_url
}

# 发送登录请求
response = session.post(login_url, data=login_data, headers=headers)

# 检查登录是否成功
if response.status_code == 200 and "成功标识" in response.text:  # 根据实际情况修改成功标识
    print("登录成功！")
    
    #
