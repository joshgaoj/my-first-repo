import requests
from bs4 import BeautifulSoup

from datetime import datetime
import os
import time

# 定义要抓取的页面范围
start_page = 1
end_page = 999
# 获取当前日期和时间，并格式化为 YYYYMMDDHHMM 的形式
current_time_str = datetime.now().strftime('%Y%m%d%H%M')
# 获取当前日期，并格式化为 DD/MM/YY 的形式
current_date_str = datetime.now().strftime('%y/%m/%d')
print(current_date_str)
# 创建输出目录
output_dir = 'out'
os.makedirs(output_dir, exist_ok=True)

# 过滤条件
filter_keywords = ["規約","補足資料","登録書","主要株主","業績の差異","一部変更","参考資料","Delayed","株主総会","定款一部変更","定款の一部変更","有価証券","決算内容"
                   "上場ETF","上場ＥＴＦ","月次","取締役","役員","剰余金","決算短信","業績予想の修正","株主提案","経営体制","決算説明","ミナー開催","上場投資信託"
                    ,"上場申請のため","通期決算説明資料","会社分割","電子提供措置事項","停止期間","交付書面","定時株主招集","計算書類","合併完了","上場廃止","連結業績"
                    ,"株式報酬","支配株主等","決算補足説明資料","人事","新株予約権","取得状況および取得終了","取得価額","取得価額","連結普通株式","資金の借入","監査役の退任"
                    ,"会計監査人","固定資産の譲渡","代表理事の異動","決算の概況","決算説明資料","内部統制","投資信託約款",
                    "四半期決算","日々の開示事項","分配金のお知らせ","立会外分売実施","報告書","事後開示書類","ＥＴＦの受益権"
                    ,"収益分配のお知らせ","本社移転","保有株式","営業外収益","株式譲渡","特別利益の","運用体制","統合レポート","販売用不動産","IRセミナー",
                    "総会決議","説明会","決算短信","資本金","公開買付","記者会見資料","一部訂正","決算説明動画","連結総資産","公認会計士"
                    ,"事業計画及び成長可能性","社外監査役","定款","買収への対応方針","収益分配金見込","法定事前開示書類","簡易株式交換","資本準備","決算質疑","剰余金"
                    ,"特別調査委員会","監査役","営業所の開設","資本コスト","持株会","[Updated]","財務会計","親会社等","約款","上場維持"]


# 英文字符集
english_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,0123456789-&'（）()'「」’")

# 加粗关键字
red_keywords = ["提携","大口","受注","新製品","株式処分","特許","開始","関連会社化","新設","株主優待","上場承認","分割","株式取得","買付行為","配当","料金改定","株式発行"]

# 检查字符串是否完全为英文
def is_fully_english(text):
    return all(c in english_chars for c in text.replace(" ", ""))

# 开始构建HTML内容
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Disclosures</title>
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
        .red {{
            color: red;
        }}
    </style>
</head>
<body>
    <h1>Disclosures</h1>
    <table>
        <tr>
            <th>区分</th>
            <th>Code</th>
            <th>Company Name</th>
            <th>Disclosure</th>
            <th>Date</th>
        </tr>
"""
# 遍历每个页面
stop_processing = False

# 遍历每个页面
for page in range(start_page, end_page + 1):
    if stop_processing:
        break   
    url = f'https://kabutan.jp/disclosures/?kubun=&page={page}'
    
    try:
        # 发出HTTP GET请求
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # 如果请求不成功, 抛出HTTPError异常
        
        print(f"Successfully fetched page {page}")
        
        # 解析网页内容
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找特定的表格
        table = soup.find('table', class_='stock_table')
        if table:
            rows = table.find_all('tr')
            
            if rows:  # 至少有一个行
                print(f"Found {len(rows)} rows of data in table.")
                
                # 输出每一行数据
                for row in rows[1:]:  # 忽略表头行
                    cols = row.find_all(['td', 'th'])  # 处理可能包含的th元素
                    if len(cols) >= 5:
                        stock_code = cols[0].find('a').text.strip() if cols[0].find('a') else 'N/A'
                        company_name = cols[1].text.strip()
                        disclosure_tag = cols[4].find('a')
                        disclosure = disclosure_tag.text.strip() if disclosure_tag else 'N/A'
                        link = disclosure_tag['href'] if disclosure_tag else 'N/A'
                        date = cols[5].find('time').text.strip() if len(cols) > 5 and cols[5].find('time') else 'N/A'
                        # 检查日期是否与当前日期相同
                        if date.split()[0] != current_date_str:
                            print(f"Date {date} is not today's date. Stopping the program.")
                            stop_processing = True
                            break
                        # 过滤条件
                        if any(keyword in disclosure for keyword in filter_keywords):
                            continue
                        if is_fully_english(disclosure):
                            continue
                        
                        # 判断是否需要变红色
                        red_text = any(keyword in disclosure for keyword in red_keywords)
                        # 提取时间部分
                        time_str = date.split()[1]

                        # 将时间字符串转换为时间对象
                        time_obj = datetime.strptime(time_str, '%H:%M').time()

                        # 定义时间范围
                        start_time = datetime.strptime('11:29', '%H:%M').time()
                        end_time = datetime.strptime('12:29', '%H:%M').time()
                        start_timeB = datetime.strptime('12:30', '%H:%M').time()
                        end_timeB = datetime.strptime('15:00', '%H:%M').time()
                        end_timeA = datetime.strptime('11:29', '%H:%M').time()
                        # 检查时间是否在范围内
                        if end_timeB <= time_obj:
                            sta = "■■■■"
                        elif start_timeB < time_obj < end_timeB:
                            sta = "AFT"
                        elif start_time < time_obj < end_time:
                            sta = "△△△"
                        elif time_obj < end_timeA:
                            sta = "MON"
                        else:
                            sta = "??"
                        # 构建HTML表格行
                        row_html = f"""
                        <tr>
                            <td>{sta}</td>
                            <td><a href="https://kabutan.jp/stock/?code={stock_code}" target="_blank">{stock_code}</a></td>
                            <td>{company_name}</td>
                            <td><a href="{link}" target="_blank" {'class="red"' if red_text else ''}>{disclosure}</a></td>
                            <td>{date}</td>
                        </tr>
                        """
                        
                        html_content += row_html
                    else:
                        print(f"Unexpected number of columns: {len(cols)} in row: {row}")
                         # 如果标志被设置，处理完当前表格后停止
                if stop_processing:
                    break
        else:
            print("No table found on the page.")
                
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
html_file_name = os.path.join(output_dir, f'disc{current_time_str}.html')
with open(html_file_name, 'w', encoding='utf-8') as html_file:
    html_file.write(html_content)

print(f"Crawling finished. Data saved to {html_file_name}.")