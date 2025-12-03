import requests
from bs4 import BeautifulSoup
import csv
import time

# 定义要抓取的页面范围
start_page = 1
end_page = 5

# 获取当前日期，并格式化为 DD/MM/YY 的形式
current_date_str = datetime.now().strftime('%d/%m/%y')
# 过滤条件
filter_keywords = ["登録書","主要株主","業績の差異","一部変更","参考資料","Delayed","株主総会招集通知", "定時株主総会","定款一部変更","定款の一部変更","決算説明会資料","上場ETF","上場ＥＴＦ","コーポレート・ガバナンスに関する報告書",
                    "月次","中期経営計画","取締役の異動","独立役員届出書","役員の異動","剰余金の配当","決算短信〔日本基準","業績予想の修正","役員人事","株主提案"
                    ,"上場申請のため","四半期報告書","個人投資家向け説明会","決算説明会","通期決算説明資料","会社分割","電子提供措置事項","交付書面省略事項","臨時株主総会"
                    ,"株式報酬","支配株主等","自己株式処分","決算補足説明資料","人事異動","新株予約権","取得状況および取得終了","取得価額","取得価額","連結普通株式","資金の借入","監査役の退任","自己株式の処分"
                    ,"自己株式の取得状況","自己株式の取得","会計監査人","固定資産の譲渡","代表理事の異動","決算の概況","自己株式","決算説明資料","取締役候補者",
                    "自己株式の消却完了","保有状況報告書","四半期決算","日々の開示事項","取締役及び監査等委員","分配金のお知らせ","立会外分売実施","役員体制","IR説明会"
                    ,"収益分配のお知らせ","本社移転","剰余金配当","保有株式","営業外収益","株式譲渡","取締役および監査役","コーポレート・ガバナンス報告書","決算短信","取締役会","資本金"]


# 英文字符集
english_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,0123456789-&'（）()")
# 加粗关键字
red_keywords = ["提携","大口","受注"]


# 检查Disclosure列是否为英文
def is_english(text):
    return all(ord(char) < 128 for char in text)

# 打开CSV文件准备写入
with open('filtered_disclosures.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # 写入表头
    writer.writerow(['Stock Code', 'Company Name','Disclosure', 'Date Time'])
    
    # 遍历每个页面
    for page in range(start_page, end_page + 1):
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
                for row in rows:
                    cols = row.find_all(['td', 'th'])
                    if len(cols) == 6:
                        # 确保每个元素存在并且有我们需要的子元素
                        stock_code = cols[0].find('a').text.strip() if cols[0].find('a') else 'N/A'
                        company_name = cols[1].text.strip() if cols[1] else 'N/A'
                        #market = cols[2].text.strip() if cols[2] else 'N/A'
                        #category = cols[3].text.strip() if cols[3] else 'N/A'
                        disclosure = cols[4].find('a').text.strip() if cols[4].find('a') else 'N/A'
                        date_time = cols[5].find('time').text.strip() if cols[5].find('time') else 'N/A'
                        if date_time.strftime('%m/%d') == current_date_str:
                                print("Data date matches today's date. Exiting program.")
                                exit()
                        # 检查是否需要过滤
                        if not is_english(disclosure) and not any(keyword in disclosure for keyword in exclude_keywords):
                            writer.writerow([stock_code, company_name, disclosure, date_time])
                            print(f"Filtered - Stock Code: {stock_code}, Company Name: {company_name}, Disclosure: {disclosure}, Date Time: {date_time}")
                    else:
                        print(f"Unexpected number of columns: {len(cols)} in row: {row}")
                    
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch page {page}: {e}")
        
        # 延时一段时间以避免对服务器造成过大压力
        time.sleep(2)

print("Crawling finished. Filtered data saved to filtered_disclosures.csv.")
