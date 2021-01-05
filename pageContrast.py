import difflib
import yagmail
import time
import json
import requests

'''
    项目说明：
    1、通过批量对新文件和旧文件的difflib对比，返回html对比报告。
    2、将对比的结果出现大量差异的则通过电子邮件将html报告作为附件发送。  (该功能暂未对接)
'''
# 对比两个文件的差异
class pageContrast:
    def __init__(self, data, line):
        self.diff = difflib.HtmlDiff()
        self.line = line
        self.newAddr = "./newDir/" + line + ".html"
        self.usedAddr= "./usedDir/"+ line + ".html"
        self.getResult()
    def getFile(self):
        self.newFile  = open(self.newAddr, 'r', encoding='utf-8')
        self.usedFile = open(self.usedAddr, 'r', encoding='utf-8')
    def comparison(self):
        self.getFile()
        self.result = self.diff.make_file(self.usedFile.read().splitlines(),self.newFile.read().splitlines())
    def getResult(self):
        self.fileResult = open('./diff/'+ self.line +'.html', 'w', encoding='utf-8')
        self.comparison()
        self.fileResult.write(self.result)
        self.fileResult.close()
        self.newFile.close()
        self.usedFile.close()
class searchs:
    def __init__(self, data, line):
        self.diff = difflib.HtmlDiff()
        self.line = line
        self.data = data
        self.newAddr = "./newDir/" + line + ".html"
        self.usedAddr = "./usedDir/" + line + ".html"
        self.copyUsed()
        self.newFile.close()
        self.usedFile.close()
    def copyUsed(self):
        self.newFile = open(self.newAddr, 'r+', encoding='utf-8')
        self.usedFile = open(self.usedAddr, 'w+', encoding='utf-8')
        self.usedFile.write(self.newFile.read()) # 替换文件
        self.download()
    def download(self):
        res = requests.post(self.data[line]['urls'])
        res.encoding='utf-8'
        self.newFile.seek(0)
        res = res.text
        self.newFile.write(res)

# 自动邮件脚本 -=> emailAuto.py

if __name__ == '__main__':
    file = open('monitoringList.json', 'r')
    data = json.load(file)['list']
    for line in data.keys():
        searches = searchs(data,line)
        pageContrasts = pageContrast(data,line)

    file.cloas()
    ''' # monitoringList.json
        {
          "list": {
            "text" : {
              "urls": "http://www.baidu.com/",
              "updateTime" : "",
              "updateNum"  : "0" ,
              "remarks"    : ""
            }
          }
        }
    '''
