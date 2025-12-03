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

# 打印所有隐藏输入字段
hidden_inputs = soup.find_all('input', {'type': 'hidden'})
for input_tag in hidden_inputs:
    print(f"Name: {input_tag.get('name')}, Value: {input_tag.get('value')}")

# 假设CSRF令牌在一个名为_csrf_token的隐藏字段中
# 你需要找到实际的CSRF令牌字段名并替换下面的_csrf_token
csrf_token_name = '_csrf_token'  # 替换为实际的CSRF令牌字段名

# 检查找到的CSRF令牌字段
csrf_token_value = None
for input_tag in hidden_inputs:
    if input_tag.get('name') == csrf_token_name:
        csrf_token_value = input_tag.get('value')
        break

if csrf_token_value is None:
    print("未找到CSRF令牌，请检查隐藏字段名")
else:
    # 准备登录数据
    login_data = {
        'username': 'your_username',  # 替换为你的用户名
        'password': 'your_password',  # 替换为你的密码
        csrf_token_name: csrf_token_value,  # 添加CSRF令牌
        # 根据登录页面的表单字段名称替换
        'other_form_fields': 'other_values'
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

        # 获取目标页面的内容
        response = session.get(target_url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # 根据需要解析页面内容
            # 例如，抓取特定的表格数据
            table = soup.find('table', {'id': 'your_table_id'})  # 替换为实际的表格ID
            for row in table.find_all('tr'):
                columns = row.find_all('td')
                for column in columns:
                    print(column.text.strip())
    else:
        print("登录失败！")
        print(response.text)  # 打印响应内容以帮助调试
