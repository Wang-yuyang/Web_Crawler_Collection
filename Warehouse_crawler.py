#! python3

import requests
import time, datetime
import json
from colorama import Fore,Back,Style,init
from bs4 import BeautifulSoup

process = 0
output  = 0


def req(type,addr,data='',**args):
    if type == 'get':
        try:
            responses = requests.get(addr,timeout=50)
        except requests.exceptions.RequestException as e:
            pass
    elif type == 'post':
        try:
            responses = requests.post(addr,timeout=50)
        except requests.exceptions.RequestException as e:
            pass
    return responses

def access(url_addr):
    # print("access")
    for i in url_addr:
        print(i['git_addr'])
        responses = req('get',i['git_addr'])
        if responses.status_code == 200:
            print("[SUCCESS]" + " %s [status] %s"%(str(i['git_addr']), str(responses.status_code)))
            i['git_addr'] = i['git_addr'] + '/commits/'
            commits(i)
        else :
            print(Fore.BLACK + Back.RED + "[ERROR]   "+"%s [status] %s"%(str(i['git_addr']), str(responses.status_code)))
            i['code'] = responses.status_code
            # return 

def commits(addr):
    url = addr['git_addr']
    responses = req('get', url)
    if responses.status_code != 200:
        print("[SUCCESS] %s [status] %s"%(str(url), str(responses.status_code)))
        addr['code'] = responses.status_code
        return 
    text = BeautifulSoup(responses.text, "html.parser")
    # 判断空仓库
    if "This repository is empty." in text:
        print(print(Fore.RED + Back.WHITE +"%s 的仓库内容爬取过程中发现告警[This repository is empty.]"%(addr['username'])))
        return
    # commits_all_dict = []
    
    all_commits = text.find_all(class_='TimelineItem-body')
    
    # 展露细节内容的
    try:
        for texts in all_commits:
            dateBar = texts.find(class_='text-normal').get_text()[11:] # 日期
            # 我们获取的日期格式是标准的英文格式日期"Nov 26, 2020"，所以我们需要进行日期的转换
            date = datetime.datetime.strptime(dateBar, '%b %d, %Y').strftime('%Y年%m月%d日')
            commits_second = 0
            if process:
                print("\n=================[%s]================="%(str(date)))
            all_commits_find = texts.ol.find_all('li')
            for commits_find in all_commits_find:
                commits_dict = {
                    'commits_auth' : commits_find.div.find('div',class_='d-flex').find('div',class_='f6').find(class_='commit-author').get_text(),
                    'commits_time' : commits_find.find('relative-time')['datetime'],  # 当前日期所提交的内容  
                    'commits_href' : "https://github.com" + commits_find.div.p.a['href'],
                    # 我们的text中式把summary和description内容融合在一起的于是我们需要把他们分开
                    'commits_summary' : commits_find.div.p.a['aria-label'][:len(commits_find.div.p.a.get_text())] ,
                    'commits_description' :  commits_find.div.p.a['aria-label'][len(commits_find.div.p.a.get_text()):].strip()
                }
                # commits_all_dict.append(commits_dict)
                commits_second += 1
                # 处理爬取数据的输出
                if process :
                    print("\n-----------------[%s]-----------------"%(commits_dict['commits_auth']))
                    print ("[提交时间] %s \n[提交代码] %s\n[提交主题] %s\n[提交描述] %s"
                                %(commits_dict['commits_time'], commits_dict['commits_href'], 
                                commits_dict['commits_summary'], commits_dict['commits_description']))
        print(Fore.BLACK + Back.WHITE +"%s 于 %s 共计提交了 %s 次代码"%(addr['username'], date, commits_second))
                
        # 处理分页爬取
        next_a = text.find(class_='paginate-container').find_all('a')
        if  len(next_a) and next_a[-1].get_text() == 'Older':
            print("------next page------")
            addr['git_addr'] = next_a[-1]['href']
            commits(addr)
    except Exception as e:
        print(print(Fore.RED + Back.WHITE +"%s 的仓库爬取过程中发生错误."%(addr['username'])))
        return

def main():
    global process
    url_addr = [
        {
            'username' : '清无',
            'git_addr' : 'https://github.com/litbird0/elevator',
            'start'    : '', 
            'commins'  : [],
        },
        {
            'username' : '曾经未曾',
            'git_addr' : 'https://github.com/1564820398/cjwc_dianti',
            'start'    : '', 
            'commins'  : [],
        },
        {
            'username' : '金一二',
            'git_addr' : 'https://github.com/flyhehe/Group_work',
            'start'    : '', 
            'commins'  : [],
        },
        {
            'username' : '丧丧的3',
            'git_addr' : 'https://github.com/wlh1024/testgit',
            'start'    : '', 
            'commins'  : [],
        },
        {
            'username' : '2.9',
            'git_addr' : 'https://github.com/1185366392/Calendar',
            'start'    : '', 
            'commins'  : [],
        },
        {
            'username' : 'Fancy',
            'git_addr' : 'https://github.com/Fancy123-cell/Colorful-calender',
            'start'    : '', 
            'commins'  : [],
        },
        {
            'username' : '擎空',
            'git_addr' : 'https://github.com/Reyourn/myelevator',
            'start'    : '', 
            'commins'  : [],
        },
        {
            'username' : '开空调',
            'git_addr' : 'https://github.com/73Hz/The-story-of-elevator',
            'start'    : '', 
            'commins'  : [],
        },
        {
            'username' : '小嫦娥',
            'git_addr' : 'https://github.com/Answerisyou/Answer',
            'start'    : '', 
            'commins'  : [],
        },
        {
            'username' : '像梦一样',
            'git_addr' : 'https://github.com/WuShiRenf/Dome',
            'start'    : '', 
            'commins'  : [],
        },
        {
            'username' : 'oneo',
            'git_addr' : 'https://github.com/oneo-10/dianti-oneo',
            'start'    : '', 
            'commins'  : [],
        },
    ]

    Webcrawler_key = "mirror"
    if input("请输入爬虫Key:") != Webcrawler_key:
        print(Fore.RED + Back.WHITE + "Key错误!")
        time.sleep(10)
        exit()

    if input("是否爬取commits细节(Y/N):").upper() == "Y":
        process = 1
    else :
        process = 0

    if input("指定爬取单个仓库").upper() == "Y":
        url_addr = [{
            'username' : 'alone',
            'git_addr' : input("仓库名(请输入完整的项目地址)"),
            'start'    : '', 
            'commins'  : [],
        }]
        

    access(url_addr)
    print("[OK] 爬行结束 ...")
    if input("是否关闭当前窗口(Y/N):").upper() == "Y":
        exit()
    else :
        pass
    exit()


if __name__ == "__main__":
    init(autoreset=True)
    print("""
__        __             _                                                     _           
\ \      / /_ _ _ __ ___| |__   ___  _   _ ___  ___     ___ _ __ __ ___      _| | ___ _ __ 
 \ \ /\ / / _` | '__/ _ \ '_ \ / _ \| | | / __|/ _ \   / __| '__/ _` \ \ /\ / / |/ _ \ '__|
  \ V  V / (_| | | |  __/ | | | (_) | |_| \__ \  __/  | (__| | | (_| |\ V  V /| |  __/ |   
   \_/\_/ \__,_|_|  \___|_| |_|\___/ \__,_|___/\___|___\___|_|  \__,_| \_/\_/ |_|\___|_|   
                                                  |_____|                                  
    version: 0.2(Deta)
    release: November 30, 2020
    author : Mirror(mirrorwangyuyang@gmail.com)
-------------------------------------------------------------------------------------------
    """)
    main()