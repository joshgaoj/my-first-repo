import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

headers = {
    "User-Agent": "Mozilla/5.0"
}

# 关键词 -> 分类名
KEYWORDS = {
    "アナリスト予想": "アナリスト予想",
    "レーティング変更観測": "レーティング変更観測",
    "アナリスト評価": "アナリスト評価"
}

# 分类结果字典
results = {kw: [] for kw in KEYWORDS}

def clean_title(title: str) -> str:
    """
    去掉标题末尾的来源文字，但保留日期。
    例如：
    '9/3アイフィス株予報' -> '9/3'
    """
    # 匹配末尾日期 + 来源文字
    match = re.search(r'(\d{1,2}/\d{1,2})\S*$', title)
    if match:
        date_part = match.group(1)
        # 保留标题中日期前面的内容 + 日期
        title_before = title[:match.start()].rstrip("。").strip()
        return f"{title_before} {date_part}".strip()
    else:
        return title



def highlight_keywords(title: str) -> str:
    """高亮显示关键字“上方修正”"""
    return re.sub(r'(上方修正)', r'<span style="color:red;font-weight:bold;">\1</span>', title)

# 循环抓取 page=1 到 10
for page in range(1, 11):
    url = f"https://finance.yahoo.co.jp/news/stocks?vip=off&page={page}"
    print(f"正在抓取：{url}")

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"❌ 请求失败：{url} 状态码 {response.status_code}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")

    # 只抓取新闻正文链接
    articles = soup.find_all("a", href=lambda href: href and "news/detail" in href)

    for a in articles:
        title = a.get_text(strip=True)
        title = clean_title(title)          # 去掉前缀
        title = highlight_keywords(title)   # 高亮“上方修正”
        href = a['href']

        # 判断相对路径还是完整路径
        if href.startswith("http"):
            full_link = href
        else:
            full_link = f"https://finance.yahoo.co.jp{href}"

        # 根据关键词分类
        for kw in KEYWORDS:
            if kw in title:
                results[kw].append((title, full_link))
                break

# 生成 HTML
html_content = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>アナリスト関連ニュース</title>
</head>
<body>
    <h1>アナリスト関連ニュース一覧</h1>
"""

for kw, items in results.items():
    html_content += f"<h2>{KEYWORDS[kw]}</h2>\n<ul>\n"
    for title, link in items:
        html_content += f'<li><a href="{link}" target="_blank">{title}</a></li>\n'
    html_content += "</ul>\n"

html_content += """
</body>
</html>
"""

# 生成时间戳文件名
timestamp = datetime.now().strftime("%m%d%H%M")
output_file = f"newsY_{timestamp}.html"

# 保存到文件
with open(output_file, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"✅ 已保存到 {output_file}")
for kw, items in results.items():
    print(f"{KEYWORDS[kw]}: {len(items)} 条")
