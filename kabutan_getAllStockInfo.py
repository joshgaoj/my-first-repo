import requests
from bs4 import BeautifulSoup
import time

def get_stock_data(stock_code):
    url = f"https://kabutan.jp/stock/?code={stock_code}"
    
    # 发送HTTP请求
    response = requests.get(url)
    
    if response.status_code == 200:
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找具有class为si_i1_1的div元素
        divs_si_i1_1 = soup.find_all('div', class_='si_i1_1')
        
        # 提取每个div的内容，但排除包含datetime的元素
        contents_si_i1_1 = [div.text.strip() for div in divs_si_i1_1 if 'datetime' not in div.text]
        content_si_i1_1 = ", ".join(contents_si_i1_1)
        
        # 查找具有class为company_block的div元素
        div_company_block = soup.find('div', class_='company_block')
        
        # 如果找到了company_block元素
        if div_company_block:
            # 查找company_block元素下的最后一个table元素
            table = div_company_block.find_all('table')[-1]
            
            # 查找table元素下的最后一个tr元素
            last_tr = table.find_all('tr')[-1]
            
            # 提取最后一个tr的内容
            last_tr_content = last_tr.text.strip()
            
            # 输出stock_code和内容
            print(f"Stock Code: {stock_code}, Content si_i1_1: {content_si_i1_1}, Last TR Content: {last_tr_content}")
            
    else:
        print(f"Failed to retrieve data for stock code {stock_code}. Status code: {response.status_code}")

        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
               # 查找具有class为si_i1_1的div元素
        divs_si_i1_1 = soup.find_all('div', class_='si_i1_1')
        
        # 输出每个div的内容，但排除包含datetime的元素
        for div_si_i1_1 in divs_si_i1_1:
            # 检查是否包含datetime
            if 'datetime' in div_si_i1_1.text:
                continue
            
            # 输出内容
            content = div_si_i1_1.text.strip()
            print(f"Stock Code: {stock_code}, Content: {content}")
            
        # 查找具有class为company_block的div元素
        div_company_block = soup.find('div', class_='company_block')
        
        # 如果找到了company_block元素
        if div_company_block:
            # 查找company_block元素下的最后一个table元素
            table = div_company_block.find_all('table')[-1]
            
            # 查找table元素下的最后一个tr元素
            last_tr = table.find_all('tr')[-1]
            
            # 输出最后一个tr的内容
            last_tr_content = last_tr.text.strip()
            print(f"Stock Code: {stock_code}, Last TR Content: {last_tr_content}")
        
        print(f"Failed to retrieve data for stock code {stock_code}. Status code: {response.status_code}")

if __name__ == "__main__":
    # 设置要爬取的股票代码范围为0001到9999
    start_code = 8226
    end_code = 8228

    # 循环爬取数据
    for code in range(start_code, end_code):
        # 使用格式化字符串确保股票代码是四位数
        formatted_code = f"{code:04d}"
        
        # 调用爬取函数
        get_stock_data(formatted_code)
        
        # 添加延迟，等待3秒再进行下一次请求
        time.sleep(3)
