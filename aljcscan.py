#!/usr/bin/python3
# coding: utf-8

import re
import os
import html
import argparse
import requests
import subprocess
import warnings
import threading
from fake_useragent import UserAgent
from urllib.parse import quote
from termcolor import cprint
from urllib.parse import urlparse
warnings.filterwarnings(action='ignore')
requests.DEFAULT_RETRIES = 6
# warnings.filterwarnings(action='ignore')

reconpath = "recon_domains"
scopepath = "scope_domains"

# 子域名文件
subfinder_file = "_subfinder.txt"
shuffledns_file = "_shuffledns.txt"
rapiddns_file = "_rapiddns.txt"
# 验证结果文件
sub_file_ok = "_sub_ok.txt"
# 去重后文件
anew_file = "_anew_file.txt"
# 各个域名对应标题、状态吗等信息文件
title_file = "_title.txt"


def radSpider(targetDomain,saveDir):
    #爬虫
    # scanCommand = "echo {0}|./httpx -silent -mc 200,301,302 -threads -1000 |./hakrawler -d 2 -subs > {1}".format(targetDomain, saveDir+"domain_js.txt")
    scanCommand = "echo {0}| .\httpx.exe -silent -mc 200,301,302 -threads -1000 |.\hakrawler.exe -d 2 -subs > {1}".format(targetDomain, saveDir+"domain_js.txt")
    print("\033[1;33m command>>>>>> \033[0m","\033[1;33m"+ scanCommand +"\033[0m")
    finderjs_result = subprocess.Popen(scanCommand, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=True)
    finderjs_result.wait()
    return

def All_JC(urls):
    headers={
        'User-Agent':'Mozilla/5.0 (compatible;Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html)',
        'Referer':'https://www.baidu.com/'
    }
    for url in urls:
        try:
            res=requests.get(url,headers=headers,timeout=10,verify=False).text
            respose=html.unescape(res)
            rules = []#匹配到的标签
            host=True
            for re_rules in re_rules_list:
                chashuibiao=re.findall(r'{}'.format(re_rules),respose,re.S|re.I)
                if chashuibiao !=[]:
                    rules.append(re_rules)
                    host=False
            if host ==False:
                with open("result.txt", "a") as file:
                    file.write('地址：{}\n匹配项：{}\n\n'.format(url,rules))
                print('{}:{} 存在暗链！'.format(threading.current_thread().name,url))
            else:
                print('{}:{} 未检测出'.format(threading.current_thread().name,url))
        except :
            print('{}:{}请求出错'.format(threading.current_thread().name,url))

RootPath = os.path.dirname(os.path.abspath(__file__))
savePath = "{}/{}".format(RootPath,reconpath)
# saveXrayReport = '{}\\save\\xrayReport'.format(RootPath)

targetFileName=""
plugins=""

def logo():
    logo='''
          $$\                                                      
          $$ |                                                     
 $$$$$$\  $$ |$$\  $$$$$$$\  $$$$$$$\  $$$$$$$\ $$$$$$\  $$$$$$$\  
 \____$$\ $$ |\__|$$  _____|$$  _____|$$  _____|\____$$\ $$  __$$\ 
 $$$$$$$ |$$ |$$\ $$ /      \$$$$$$\  $$ /      $$$$$$$ |$$ |  $$ |
$$  __$$ |$$ |$$ |$$ |       \____$$\ $$ |     $$  __$$ |$$ |  $$ |
\$$$$$$$ |$$ |$$ |\$$$$$$$\ $$$$$$$  |\$$$$$$$\\$$$$$$$ |$$ |  $$ |
 \_______|\__|$$ | \_______|\_______/  \_______|\_______|\__|  \__|
        $$\   $$ |                                                 
        \$$$$$$  |                                                 
         \______/ 
         Author:tom v1.0
    '''
    return logo

with open('rules.txt', 'r',encoding='utf-8') as s:
    re_rules_list = s.read().split('\n')  


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--targets', default='targets.txt',
                        help='information gathering for SubDomain')
    parser.add_argument('--files', default='files',
                        help='Save subDomain info to Files')
    parser.add_argument('--outname', default='test',
                        help='Save outname') 
    parser.add_argument('--Thread', action='store',
                        type=int, default=10,    
                        help='Thread') 
    parser.add_argument('--aljc', action='store',
                        type=bool, default=False,
                        help='Scan for sensitive words')      
    parser.add_argument('--aljcall', action='store',
                        type=bool, default=False,
                        help='Scan for all  sensitive words')        


    args = parser.parse_args()
    print(args.targets)

    try:
        print(logo())
        saveDir = "{}/{}/{}/".format(RootPath,reconpath,args.files)
        filepath = args.files

        if args.aljc:
            with open (args.targets, "r+") as f:
                urls_list = f.read().split('\n')
                All_JC(urls_list)
        if args.aljcall:
            xc = args.Thread

            with open (args.targets, "r") as f:
                for i in f.readlines():
                    domain = i.strip("\n")
                    radSpider(domain,saveDir)
                    if os.path.exists(saveDir+"domain_js.txt"):
                        with open(saveDir+"domain_js.txt", 'r') as f:
                            urls_list = f.read().split('\n')
                            urls = []   
                            twoList = [[] for i in range(xc)]
                            for i, e in enumerate(urls_list):
                                twoList[i % xc].append(e)
                            for i in twoList:
                                urls.append(i)
                            thread_list = [threading.Thread(target=All_JC, args=(urls[i],)) for i in range(len(urls))]
                            for t in thread_list:
                                t.start()
                            for t in thread_list:
                                t.join()

    except Exception as e:
        print(e)
        pass
    return

if __name__ == '__main__':
    main()

