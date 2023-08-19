from os.path import exists, split
from os import makedirs,getcwd,system
from urllib.request import urlretrieve
from sys import stdout
import urllib
import random
import ssl
import json
import zipfile
import os

myPATH = getcwd()

opener = urllib.request.build_opener()
# 构建请求头列表每次随机选择一个
ua_list = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
           'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
           'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.62',
           'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0',
           'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36 SE 2.X MetaSr 1.0'
           ]
opener.addheaders = [('User-Agent', random.choice(ua_list))]
urllib.request.install_opener(opener)


ssl._create_default_https_context = ssl._create_unverified_context

def download(url: str, path: str):
    # try:
    print(url)
    (filepath, filename) = split(path)
    if not exists(filepath):
        makedirs(filepath)

    def hook(blocknum, bs, size):  # 回调
        # blocknum数据块数量
        # bs数据块大小
        # size下载下来的总大小
        # 下载进度 = (blocknum x bs) / size
        a = int(float(blocknum * bs) / size * 100)
        if a >= 100:
            a = 100

        stdout.write("\r>>正在下载" + filename + ":" + str(a) + "%")

    urlretrieve(url=url, filename=path, reporthook=hook)
    print("\n")
    # except:
    #     print("\n由于网络原因，下载发生错误，正在尝试重新下载\n")
    #     download(url=url, path=path)

def findForgeList(mcVersion):
    Verison = []
    download("https://bmclapi2.bangbang93.com/forge/list/0/0",myPATH+"/ForgeList.json")
    Content = open("ForgeList.json").read()
    forgeList = json.loads(Content)
    for item in forgeList :
        if mcVersion == item['mcversion']:
            Verison.append(item['version'])
    return Verison
def downloadForgeInstaller(mcVersion):
    forgeVersion = findForgeList(mcVersion)
    print("查询到以下forge，默认选择最新版本")
    for i in forgeVersion:
        print(i)
    forgeVersion = forgeVersion[0]
    global forge
    forge = mcVersion+'-'+forgeVersion
    path = myPATH+"/forge-"+forge+"-installer.jar"
    # https://maven.minecraftforge.net/net/minecraftforge/forge/1.20.1-47.1.43/forge-1.20.1-47.1.43-installer.jar
    URL = "https://bmclapi2.bangbang93.com/maven/net/minecraftforge/forge/"+forge+"/forge-"+forge+"-installer.jar"
    download(URL,path)
    return path

# def unzip(forge):
#     path =  myPATH+'/Temporarily/ForgeUnZip'
#     zipFile = zipfile.ZipFile(forge)
#     for file in zipFile.namelist():
#         zipFile.extract(file, path)
#     zipFile.close()
#
# def installLibraries(path):
#     Content = json.loads(open(myPATH+'/Temporarily/ForgeUnZip/install_profile.json',"r").read())
#     for i in Content['libraries']:
#         pAth = path+'/'+i['downloads']['artifact']['path']
#         url = i['downloads']['artifact']['url']
#         url = str.replace(url,'https://maven.minecraftforge.net/','https://bmclapi2.bangbang93.com/maven/')
#         download(url,pAth)

def  installForge(mcversion):
    forgePATH = downloadForgeInstaller(mcversion)
    system('java -jar '+forgePATH)
    os.remove("forge-"+forge+"-installer.jar")
    os.remove("forge-"+forge+"-installer.jar.log")