import pandas as pd
import mysql.connector
from mysql.connector import Error

# 配置数据库连接
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'dnc.2009',
    'database': 'mysql'
}

# CSV文件路径
csv_file_path = r'C:\Users\joshg\OneDrive\デスクトップ\株価一覧\T240726.csv'

# 定义列名，将kanri3放到最后，去掉exchange列

csv_columns = [
    'getdate', 'code', 'kanri1', 'kanri2',
    'pricebegain', 'pricehigh', 'pricelow', 'priceclose', 'dekidaka', 'kanri3'
]

# 读取CSV文件，指定列名和编码为shift_jis
data = pd.read_csv(csv_file_path, names=csv_columns, encoding='shift_jis')

# 重新排序数据的列，不包括 kanri1, kanri2, kanri3
data = data.reindex(columns=['getdate', 'code', 'pricebegain', 'pricehigh', 'pricelow',
                             'priceclose', 'dekidaka', 'kanri1', 'kanri2', 'kanri3'])

# 使用 .fillna() 方法将 NaN 替换为 0
data = data.fillna(0)

# 将需要转换为整数的列转换为整数类型，先处理可能存在的 NaN 值
data['pricebegain'] = data['pricebegain'].fillna(0).astype(int)
data['pricehigh'] = data['pricehigh'].fillna(0).astype(int)
data['pricelow'] = data['pricelow'].fillna(0).astype(int)
data['priceclose'] = data['priceclose'].fillna(0).astype(int)

# 处理 dekidaka 列，将非数值数据替换为 0 或者根据需求进行处理
data['dekidaka'] = pd.to_numeric(data['dekidaka'], errors='coerce').fillna(0).astype(int)

# 连接到MySQL数据库
try:
    connection = mysql.connector.connect(**db_config)
    if connection.is_connected():
        cursor = connection.cursor()

        # 插入数据到表中，避免重复插入相同的主键组合
        for index, row in data.iterrows():
            # 检查是否已存在相同的 code 和 getdate 组合
            sql_check = "SELECT * FROM stock_data WHERE code = %s AND getdate = %s"
            values_check = (str(row['code']), str(row['getdate']))
            cursor.execute(sql_check, values_check)
            result = cursor.fetchone()

            if result:
                print(f"数据已存在，跳过插入：{row['code']} - {row['getdate']}")
            else:
                sql_insert = """INSERT INTO stock_data (code, getdate, pricebegain, pricehigh, pricelow, priceclose, dekidaka, kanri1, kanri2, kanri3)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, 0, 0, 0)"""
                values_insert = (
                    str(row['code']), str(row['getdate']), int(row['pricebegain']), int(row['pricehigh']),
                    int(row['pricelow']), int(row['priceclose']), int(row['dekidaka'])
                )
                cursor.execute(sql_insert, values_insert)
                print(f"成功插入数据：{row['code']} - {row['getdate']}")

        # 提交事务
        connection.commit()
        print("数据插入成功")

except Error as e:
    print(f"MySQL Error: {e}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL连接关闭")
