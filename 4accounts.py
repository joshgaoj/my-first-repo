import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

# 定义要抓取的页面范围
start_page = 1
end_page = 125

# 定义过滤规则
exclude_keywords =  ["下方修正", "減益"]
# 加粗关键字
red_keywords = ["配当","増配","一転","上方修正","赤字"]

# 获取当前日期的月份和日期，并格式化为 MM/DD 的形式
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
        </tr>
"""

# 遍历每个页面
stop_processing = False

for page in range(start_page, end_page + 1):
    if stop_processing:
        break
    
    url = f'https://kabutan.jp/news/marketnews/?category=3&page={page}'
    
    try:
        # 发出HTTP GET请求
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # 如果请求不成功, 抛出HTTPError异常
        
        print(f"Successfully fetched page {page}")
        
        # 解析网页内容
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找特定的表格
        tables = soup.find_all('table', class_='s_news_list mgbt0') + soup.find_all('table', class_='s_news_list mgt0')
        if tables:
            print("Found tables!")
            
            for table in tables:
                rows = table.find_all('tr')
                table_stop_processing = False  # 为每个表单独设置停止标志
                
                if rows:  # 至少有一个行
                    print(f"Found {len(rows)} rows of data in table.")
                    
                    # 输出每一行数据
                    for row in rows:
                        cols = row.find_all('td')
                        if len(cols) == 3:
                            date_time_str = cols[0].find('time').text.strip() if cols[0].find('time') else 'N/A'
                            category = cols[1].find('div').text.strip() if cols[1].find('div') else 'N/A'
                            news_tag = cols[2].find('a')
                            news = news_tag.text.strip() if news_tag else 'N/A'
                            link = news_tag['href'] if news_tag else 'N/A'
                            
                            # 过滤包含特定关键字的行
                            if any(keyword in news for keyword in exclude_keywords):
                                continue
                            
                            # 如果 date_time 的日期部分与当前日期不同，则设置标志
                            if date_time_str.split()[0] != current_date_str:
                                print("Data date does not match today's date. Marking to stop processing after this table.")
                                stop_processing = True
                                break
                            
                            # 在链接前添加https://kabutan.jp/
                            link = f'https://kabutan.jp{link}'
                            #红色粗关键字
                            bold_news = news
                            for keyword in red_keywords:
                                if keyword in news:
                                    bold_news = bold_news.replace(keyword, f'<span style="font-weight:bold; color:red;">{keyword}</span>')

                            #td_element = f'<td><a href="{link}" target="_blank">{bold_news}</a></td>'
                            # 构建HTML表格行
                            html_content += f"""
                            <tr>
                                <td>{date_time_str}</td>
                                <td>{category}</td>
                                <td><a href="{link}" target="_blank">{bold_news}</a></td>
                            </tr>
                            """
                        else:
                            print(f"Unexpected number of columns: {len(cols)} in row: {row}")
                
                # 如果标志被设置，处理完当前表格后停止
                if stop_processing:
                    break
        else:
            print("No tables found on the page.")
                
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch page {page}: {e}")
    
    # 延时一段时间以避免对服务器造成过大压力
    time.sleep(1)

# 完成HTML内容
html_content += """
    </table>
</body>
</html>
"""

# 将HTML内容写入文件
html_file_name = f'out/决算配当_{datetime.now().strftime("%Y%m%d%H%M")}.html'
with open(html_file_name, 'w', encoding='utf-8') as html_file:
    html_file.write(html_content)

print(f"Crawling finished. Data saved to {html_file_name}.")
