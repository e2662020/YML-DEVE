import os
from os import makedirs,getcwd
from urllib.request import urlretrieve  # 下载函数
from sys import stdout
from os.path import exists, split
from json import loads
from threading import Thread
import ssl
import urllib
import random
import wget

a = 0
downloadSource = "https://download.mcbbs.net/"

try:
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
    # 下载文件函数
    def download(url: str, path: str):
        try:
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
        except:
            print("\n由于网络原因，下载发生错误，正在尝试重新下载\n")
            download(url=url, path=path)

    def normalDownload(url,path=None):
        if path == None:
            path = os.getcwd()
        wget.download(url, path)


    def downloadList(Path,version):
        # 下载版本清单文件
        url = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
        # url = "https://bmclapi2.bangbang93.com/mc/game/version_manifest_v2.json"  # 国内源
        path = myPATH+"/version_manifest.json"
        try:
            os.remove("version_manifest.json")
        except:
            pass
        download(url,path)




    def Outversion(isOut=False, release=False, snapshot=False, old=False):
        # isOut是否在屏幕上输出版本列表
        # release正式版
        file = open("./version_manifest.json")
        VersionListDict = loads(file.read())
        return VersionListDict


    try:
        Outversion(isOut=True, release=True, snapshot=True, old=True)
    except:
        pass

    def isRightVersion(version: str):
        VLD = Outversion()
        flag = False  # 判断是否有这个版本
        for v in VLD["versions"]:
            if v["id"] == version:
                flag = True
        return flag


    # 下载游戏部分
    def downloadVersion(version: str, mcDir: str):
        Threads = []  # 线程池
        # mcDir.minecraft路径
        downloadList(mcDir,version)
        # 1,下载版本json文件
        if isRightVersion(version):
            VLD = Outversion()
            for v in VLD["versions"]:
                if v["id"] == version:
                    url = v["url"]
                    path = mcDir + "/versions/" + version + "/" + version + ".json"
                    if not exists(mcDir + "/versions/" + version):
                        makedirs(mcDir + "/versions/" + version)
                    url = str(url)
                    download(url=url, path=path)
                    print("版本json下载完成\n")

        # 2,下载客户端
        VersionDict = loads(open(mcDir + "/versions/" + version + "/" + version + ".json",encoding="UTF-8").read())
        url = downloadSource+"version/"+version+"/client"
        path = mcDir + "/versions/" + version + "/" + version + ".jar"
        download(url=url, path=path)
        print("游戏本体下载完成\n")

        # 3,下载依赖库
        for lib in VersionDict["libraries"]:
            # 3.1,下载普通库
            if "artifact" in lib["downloads"] and not "classifiers" in lib["downloads"]:
                url = lib["downloads"]["artifact"]["url"]
                (filepath, tempfilename) = split(lib["downloads"]["artifact"]["path"])
                if not exists(mcDir + "/libraries/" + filepath):
                    makedirs(mcDir + "/libraries/" + filepath)
                path = mcDir + "/libraries/" + lib["downloads"]["artifact"]["path"]
                url = str.replace(url,"https://libraries.minecraft.net/",downloadSource+"maven/")
                download(url=url, path=path)

            # 3.2,下载natives库
            if "classifiers" in lib["downloads"]:
                # 3.2.1,下载artifact部分
                try:
                    print("-----------------WARN:容易引发错误--------------------")
                    url = lib['downloads']["artifact"]["url"]
                    (filepath, tempfilename) = split(lib["downloads"]["artifact"]["path"])
                    if not exists(mcDir + "/libraries/" + filepath):
                        makedirs(mcDir + "/libraries/" + filepath)
                    path = mcDir + "/libraries/" + lib["downloads"]["artifact"]["path"]
                    url = str.replace(url,"https://libraries.minecraft.net/",downloadSource+"maven/")
                    print(url)
                    download(url=url, path=path)
                    print("---------------------------------------------------")
                except KeyError:
                    # pass
                    return "error"
                # 3.2.2,下载classifiers部分
                for cl in lib["downloads"]["classifiers"].values():
                    url = cl["url"]
                    (filepath, tempfilename) = split(cl["path"])
                    if not exists(mcDir + "/libraries/" + filepath):
                        makedirs(mcDir + "/libraries/" + filepath)
                    path = mcDir + "/libraries/" + cl["path"]
                    url = str.replace(url, "https://libraries.minecraft.net/", downloadSource+"maven/")
                    download(url=url, path=path)
        print("\n依赖库下载完成\n")

        # 4,下载资源索引
        url = VersionDict["assetIndex"]["url"]
        path = mcDir + "/assets/indexes/" + VersionDict["assetIndex"]["id"] + ".json"
        url = str.replace(url,"https://piston-meta.mojang.com/", downloadSource)
        download(url=url, path=path)
        print("\资源索引文件下载完成下载完成\n")

        # 5,下载资源文件
        # 5.1,解析资源索引文件
        for object in loads(open(path, "r").read())["objects"].values():
            url = f"https://bmclapi2.bangbang93.com/assets/{object['hash'][0:2]}/{object['hash']}"
            path = f"{mcDir}/assets/objects/{object['hash'][0:2]}/{object['hash']}"
            if not exists(path):
                def runnable():
                    download(url=url, path=path)

                thread = Thread(target=runnable)
                thread.start()
                Threads.append(thread)
                # 5.1.1,少许停顿. 避免冲突
                i = 7
                while i > 0:
                    i -= 1

        # 5.2,等待线程池中所有线程进行完成
        for th in Threads:
            th.join()


    if not exists(".minecraft"):
        makedirs(".minecraft")
except FileExistsError:
    pass
