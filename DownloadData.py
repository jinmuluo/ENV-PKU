import urllib
from bs4 import BeautifulSoup
import requests

#加入Cookie和User-Agent信息
Cookieinfo = "_ga=GA1.2.191036712.1513054631; _ga=GA1.4.191036712.1513054631; _ga=GA1.3.191036712.1513054631; __utma=259910805.584284371.1517572701.1524746115.1528784104.5; __utmz=259910805.1528784104.5.5.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _ceir=1; _ceg.s=pizjwy; _ceg.u=pizjwy; _urs-gui_session=823990a44be1947d9de356e9424f8a8d; urs_user_already_logged=yes; _ceg.s=pizk25; _ceg.u=pizk25"
User = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"
headers = {'Cookie': Cookieinfo,
           'User-Agent': User
           }

rawurl = 'https://e4ftl01.cr.usgs.gov/PullDir/030463600287878'
content = urllib.request.urlopen(rawurl).read().decode('ascii')  #获取页面的HTML
soup = BeautifulSoup(content, 'lxml')
url_cand_html = [soup.find_all('a')]   #定位到存放url的标号为content的div标签
urls = []
t=soup.select('a')
for i in t:
    urls.append(i.get('href'))

f = open('G:/2007-2014.txt', 'w')
print('you have', len(urls), 'files need to be downloaded!')
for i, url in enumerate(urls):
    if urls[i][-3:] != 'hdf':
        continue
    print("This is file"+str(i+1)+" downloading! You still have "+str(len(urls)-i-1)+" files waiting for downloading!!")
    f.write(rawurl + '/' + urls[i] + '\n')
    # file_name = "G:/2000.txt"  #文件保存位置+文件名
    # r = requests.get(rawurl+url, headers=headers)
    # with open(file_name, "wb") as code:
    #    code.write(r.content)



