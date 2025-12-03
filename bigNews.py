import requests
from bs4 import BeautifulSoup
import csv
import time
from datetime import datetime

# 定义要抓取的页面范围
start_page = 1
end_page = 25

# 定义过滤规则
exclude_keywords = ["個人投資家の予想", "前場のランキング","＜注目銘柄＞","【ストップ高／ストップ安】","＜注目銘柄＞","前日に動いた銘柄"]

# 获取当前日期的月份和日期，并格式化为 MM-DD 的形式
current_date_str = datetime.now().strftime('%m/%d')

# 打开CSV文件准备写入
csv_file_name = f'out/marketnews_{datetime.now().strftime("%Y%m%d%H%M")}.csv'
with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # 写入表头
    writer.writerow(['Date Time', 'Category', 'News', 'Link'])

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
            table = soup.find('table', class_='s_news_list mgbt0')
            if table:
                print("Found table!")
                
                rows = table.find_all('tr')
                if len(rows) > 1:  # 至少有一个表头行
                    print(f"Found {len(rows) - 1} rows of data in table.")  # 减去表头行
                    
                    # 输出表头
                    header_row = rows[0]
                    print("Header Row:")
                    print(header_row)
                    
                    # 输出每一行数据
                    for row in rows[1:]:
                        print("Data Row:")
                        print(row)
                        
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
                            link = f'https://kabutan.jp{link}'
                            
                            writer.writerow([date_time_str, category, news, link])
                            print(f"Successfully wrote row to CSV: Date Time: {date_time_str}, Category: {category}, News: {news}, Link: {link}")
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

print(f"Crawling finished. Data saved to {csv_file_name}.")
