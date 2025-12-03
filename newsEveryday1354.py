import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

# 定义要抓取的页面范围
start_page = 1
end_page = 25

# 定义过滤规则
#exclude_keywords = ["個人投資家の予想", "前場のランキング"]
exclude_keywords = ["こう"]
# 获取当前日期的月份和日期，并格式化为 MM-DD 的形式
current_date_str = datetime.now().strftime('%m/%d')

# 开始构建HTML内容
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Market News</title>
    <style>
        table {{
            border-collapse: collapse;
            width: 100%;
        }}
        th, td {{
            border: 1px solid black;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
        }}
    </style>
</head>
<body>
    <h1>Market News</h1>
    <table>
        <tr>
            <th>Date Time</th>
            <th>Category</th>
            <th>News</th>
            <th>Link</th>
        </tr>
"""

# 遍历每个页面
for page in range(start_page, end_page + 1):
    url = f'https://kabutan.jp/news/marketnews/?category=2&page={page}'
    
    try:
        # 发出HTTP GET请求
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # 如果请求不成功, 抛出HTTPError异常
        
        print(f"Successfully fetched page {page}")
        
        # 解析网页内容
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找特定的表格
        table = soup.find('table', class_='s_news_list mgbt0') or soup.find('table', class_='s_news_list mgt0')  # 添加了CSS类名 's_news_list mgt0'
        if table:
            print("Found table!")
            
            rows = table.find_all('tr')
            if len(rows) > 1:  # 至少有一个表头行
                print(f"Found {len(rows) - 1} rows of data in table.")  # 减去表头行
                
                # 输出每一行数据
                for row in rows[1:]:
                    cols = row.find_all('td')
                    if len(cols) == 3:
                        date_time_str = cols[0].find('time').text.strip() if cols[0].find('time') else 'N/A'
                        category = cols[1].find('div').text.strip() if cols[1].find('div') else 'N/A'
                        news = cols[2].find('a').text.strip() if cols[2].find('a') else 'N/A'
                        link = cols[2].find('a')['href'] if cols[2].find('a') else 'N/A'
                        
                        # 解析日期时间字符串为 datetime 对象
                        date_time = datetime.strptime(date_time_str, '%m/%d %H:%M')
                        
                        # 过滤包含特定关键字的行
                        if any(keyword in news for keyword in exclude_keywords):
                            continue
                        
                        # 如果 date_time 的日期部分与当前日期不同，则退出所有循环
                        if date_time.strftime('%m/%d') != current_date_str:
                            print("Data date does not match today's date. Exiting all loops.")
                            break
                        
                        # 在链接前添加https://kabutan.jp/
                        link = f'https://kabutan.jp/{link}'
                        
                        # 构建HTML表格行
                        html_content += f"""
                        <tr>
                            <td>{date_time_str}</td>
                            <td>{category}</td>
                            <td>{news}</td>
                            <td><a href="{link}" target="_blank">{link}</a></td>
                        </tr>
                        """
                    else:
                        print(f"Unexpected number of columns: {len(cols)} in row: {row}")
            else:
                print("No data rows found in table.")
        else:
            print("No table found on the page.")
                
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch page {page}: {e}")
    
    # 延时一段时间以避免对服务器造成过大压力
    time.sleep(2)
    
    # 检查标志，如果已经退出所有循环，则立即退出程序
    if date_time.strftime('%m/%d') != current_date_str:
        print("Exiting program.")
        break

# 完成HTML内容
html_content += """
    </table>
</body>
</html>
"""

# 将HTML内容写入文件
html_file_name = f'out/marketnews_{datetime.now().strftime("%Y%m%d%H%M")}.html'
with open(html_file_name, 'w', encoding='utf-8') as html_file:
    html_file.write(html_content)

print(f"Crawling finished. Data saved to {html_file_name}.")
