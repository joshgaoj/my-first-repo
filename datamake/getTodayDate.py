import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

# 从 codelist.py 中导入股票代码列表
from codelist import codes

def fetch_stock_data(code):
    url = f'https://kabutan.jp/stock/?code={code}'
    response = requests.get(url)
    response.raise_for_status()  # 检查请求是否成功

    soup = BeautifulSoup(response.text, 'html.parser')

    data = {
        'code': code,
        '前日終値': None,
        '始値': None,
        '高値': None,
        '安値': None,
        '終値': None,
        '出来高': None  # 添加出来高字段
    }

    try:
        # 输出 kobetsu_left_div 的内容
        kobetsu_left_div = soup.find('div', id='kobetsu_left')
        if kobetsu_left_div:
            # 抽取前日終値
            zenzitsu_owarine_element = kobetsu_left_div.find('dt', string='前日終値')
            if zenzitsu_owarine_element:
                zenzitsu_owarine = zenzitsu_owarine_element.find_next_sibling('dd').get_text(strip=True)
                data['前日終値'] = zenzitsu_owarine.split(' ')[0].replace(',', '')

            # 抽取表格中的数据
            table = kobetsu_left_div.find('table')
            if table:
                rows = table.find_all('tr')
                for row in rows:
                    th = row.find('th', scope='row')
                    if th:
                        th_text = th.get_text(strip=True)
                        td = row.find('td')
                        if td:
                            td_text = td.get_text(strip=True).replace(',', '')
                            if th_text == '始値':
                                data['始値'] = td_text
                            elif th_text == '高値':
                                data['高値'] = td_text
                            elif th_text == '安値':
                                data['安値'] = td_text
                            elif th_text == '終値':
                                data['終値'] = td_text
            
            # 添加出来高数据处理
            soudaikou = soup.find('th', string='出来高')
            if soudaikou:
                data['出来高'] = soudaikou.find_next('td').get_text(strip=True).replace('株', '').replace(',', '')

        else:
            print(f'Error: Unable to find div with id="kobetsu_left" for code {code}')

    except Exception as e:
        print(f'Error fetching data for code {code}: {e}')

    return data

# 主程序
def main():
    # 生成CSV文件名
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f'todaydata{now}.csv'

    # 创建一个空的DataFrame并保存到CSV文件
    df = pd.DataFrame(columns=['code', '前日終値', '始値', '高値', '安値', '終値', '出来高'])
    df.to_csv(filename, index=False, encoding='utf-8-sig')

    # 逐条处理股票代码并写入CSV文件
    for code in codes:
        print(f'正在处理股票代码: {code}')  # 打印当前处理的股票代码
        stock_data = fetch_stock_data(code)
        if stock_data:
            df = pd.DataFrame([stock_data])
            df.to_csv(filename, mode='a', header=False, index=False, encoding='utf-8-sig')
        time.sleep(1)  # 添加一秒钟的延迟

if __name__ == '__main__':
    main()
