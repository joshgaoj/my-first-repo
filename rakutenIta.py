#!/usr/bin/python3
# coding: utf-8

from __future__ import print_function

import codecs
import csv
import datetime
import io
import json
import numpy as np
import os
from os import listdir
import re
import requests
import shutil
from time import sleep
import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)
import sys
from bs4 import BeautifulSoup


def loadJsonData(path, arrFlg=False):
   jsonData = {}
   arrData = []

   if os.path.exists(path):
      # Relative Path
      with open(path, 'r', encoding='utf-8') as infile:
         if arrFlg:
            arrData = json.load(infile)
         else:
            jsonData = json.load(infile)

   if arrFlg:
      return arrData
   else:
      return jsonData


def crawler():
   global loginInfo

   headers = requests.utils.default_headers()
   headers.update({
      'Host': 'member.rakuten-sec.co.jp',
      'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Language': 'en-US,en;q=0.5',
      'Accept-Encoding': 'gzip, deflate, br',
      # 'Referer': 'https://www.rakuten-sec.co.jp/',
      'Content-Type': 'application/x-www-form-urlencoded',
      'Connection': 'keep-alive',
      'Upgrade-Insecure-Requests': '1'
      # Content-Length: 44
   })

   # セッションの作成
   session = requests.session()

   try:
      r = session.post('https://member.rakuten-sec.co.jp/app/MhLogin.do', data=loginInfo, headers=headers, verify=False) #requestsを使って、webから取得
      # print(r.headers['Set-Cookie'])
      # print(r.text)
      sleep(3)
      print(r.text)  # 输出返回的 HTML
      a = re.search("(logout.do;).*(\";)", r.text)


      # location.href = "/app/logout.do;BV_SessionID=5560AE7608F4B9DEF81A0C6274CEB710.411c7530";
      a = re.search("(logout.do;).*(\";)", r.text).group()
      BV_SessionID = a.split(';')[1][:-1]
      print(BV_SessionID)

      cds = ['99840', '72030', '67580']
      for cd in cds:
         target = 'https://member.rakuten-sec.co.jp/app/info_jp_prc_stock.do;' + \
            BV_SessionID + '?eventType=init&contentId=8&dscrCd=' + cd

         target2 = 'https://rakuten-sec.ifis.co.jp/index.php?inum=5004&action=3&sa=report_est&bcode=' + cd[:-1] + '&' + BV_SessionID
         # r = session.get(target, headers=headers, verify=False) #requestsを使って、webから取得
         r = requests.get(target2, verify=False)
         # print(r.headers['Set-Cookie'])
         # print(r.text)
         print(target2)

         soup = BeautifulSoup(r.text, 'lxml')                        #要素を抽出 (lxml)
         for td in soup.find_all('td', {'class':'text-long'}):
            print(td)

   except Exception as e:
      print("error: {0}".format(e), file=sys.stderr)
      exitCode = 2


def main(argv):
   # load login info
   global loginInfo
   loginInfo = loadJsonData('loginInfo.json')

   crawler()


if __name__ == "__main__":
   main(sys.argv[1:])


