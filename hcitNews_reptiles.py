#! python3

import requests
from bs4 import BeautifulSoup

import xlrd #读excel
import xlwt #写excel


def reptiles(responses,addr):
    soup = BeautifulSoup(responses.text,"html.parser")
    # print (soup.find_all(id="line_u8_0"))
    k = 0
    news_link   = []
    news_title  = []
    news_time   = []
    news_text   = []
    while True:
        key_text = "line_u8_%d"%(k)
        soup_li = soup.find(id=str(key_text))
        if key_text not in responses.text : # 遇空则break
            break
        # 获取标题
        title = soup_li.a.get_text()
        title = title[10:]
        news_title.append(title)
        # 获取时间
        time = soup_li.span.get_text()
        news_time.append(time)
        # 获取正文页
        link = soup_li.a['href']
        news_link.append(link)
        newsText_url = addr +"/"+ link
        res = requests.get(newsText_url)
        res.encoding = "utf-8"
        print("[爬取正文]%s=>[%d]"%(newsText_url,res.status_code))
        soup_newsTtext = BeautifulSoup(res.text,"html.parser")
        newsText = soup_newsTtext.find(id="vsb_content")
        news_text.append(newsText)
        # 获取正文附件并下载
        try:
            newsText_a = newsText.a['href']
            newsText_name = newsText.a.string
            newsText_link = "http://www.hcit.edu.cn" + newsText_a
            print("[附件文件]"+newsText_link)
            # res_link = requests.get(newsText_link)
            # with open(newsText_name,'wb') as code:
            #     code.write(res_link.content)
        except Exception as e:
            print("[无附件文件]")
        else:
            pass
        
        k += 1 
    # print(responses.url)
    return 


def main():
    url_addr = [
        # "http://www.hcit.edu.cn/sdxw/xyyw",
        # "http://www.hcit.edu.cn/sdxw/ybdt",
        # "http://www.hcit.edu.cn/sdxw/mtjj",
        "http://www.hcit.edu.cn/sdxw/ggtz"
    ]

    for addr in url_addr:
        page = 1
        while True:
            addr_url = addr + "/" + str(page) + ".htm"
            print(addr_url)
            responses = requests.get(addr_url)
            if responses.status_code != 200 :
                reptiles(requests.get(addr + ".htm"), addr)
                print("+++++++++++++++++++++++++++++++++[None]++++++++++++++++++++++++++++++++++++++")
                break
            responses.encoding = "utf-8"
            # 确认访问正常
            print("[爬取页面] %s [%s]"%(str(addr_url),str(responses.status_code)))
            reptiles(responses,addr)
            page += 1



if __name__ == "__main__":
    main()