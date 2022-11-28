# AljcScan

python3实现检查网页中的暗链

**原理:**通过爬虫获取网页中的URL链接，后进行访问对返回的数据包进行关键字匹配，如果匹配到了就会保存相关的网址匹配到的关键字。

## 关键字

自己可以根据想要检查的内容在根目录的rules.txt里面添加

## ![image-20221128113128787](C:\Users\pantom\AppData\Roaming\Typora\typora-user-images\image-20221128113128787.png)

需要安装chrome浏览器



## 脚本使用

参数：

```
python39.exe .\aljcscan.py -h
usage: aljcscan.py [-h] [--targets TARGETS] [--files FILES] [--outname OUTNAME] [--Thread THREAD] [--aljc ALJC]
                   [--aljcall ALJCALL]

Process some integers.

optional arguments:
  -h, --help         show this help message and exit
  --targets TARGETS  information gathering for SubDomain
  --files FILES      Save subDomain info to Files
  --outname OUTNAME  Save outname
  --Thread THREAD    Thread
  --aljc ALJC        Scan for all sensitive words
  --aljcall ALJCALL  Scan for sensitive words
```

### --targets 

指定目标

```
--targets targets,txt
```

### --Thread

线程

```
--Thread 20
```

### --aljc

默认只检测当前目标网页的返回数据

```
--aljc True
```

### --aljcall

```
--aljcall True
```

## 使用示例

### 检查当前的网页（不爬虫）

```
python39.exe .\aljcscan.py --targets .\targets.txt --aljc True
```

![image-20221128112842330](C:\Users\pantom\AppData\Roaming\Typora\typora-user-images\image-20221128112842330.png)

### 爬虫各个URL后进行检查

```
python39.exe .\aljcscan.py --targets .\targets.txt --aljcall True --Thread 20
```

![image-20221128112952392](C:\Users\pantom\AppData\Roaming\Typora\typora-user-images\image-20221128112952392.png)



## 输出

输入到当前目录 result.txt

有一些相关的网站会误报需要自己识别一下。比如下面百度健康，匹配到一些敏感关键字，彩票网站会匹配到一些博彩相关。

![image-20221128113103015](C:\Users\pantom\AppData\Roaming\Typora\typora-user-images\image-20221128113103015.png)

## 参考

https://github.com/projectdiscovery/katana

https://github.com/hakluke/hakrawler

https://github.com/projectdiscovery/httpx

DC_find 链接找不到了
