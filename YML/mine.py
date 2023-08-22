#导入库文件
import minecraft_launcher_lib
from downloadMC import downloadVersion
from downloadForge import installForge
from downloadForge import getForge
from downloadFabric import installFabric
import subprocess
import os
import platform
import webbrowser


#下载版本

#设置变量
minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()
myPATH = os.getcwd()
mcDir = minecraft_directory + "/versions/"
myOS = platform.system()
with open(myPATH+"azureAPI.txt", "r") as f:
    azureApiKey = f.read
# if myOS == "Windows":

callback = {
    "setStatus": set_status,
    "setProgress": set_progress,
    "setMax": set_max
}

def runMinecraft(minecraftVersion:str,userName:str = None):
    '''
    没啥说的，输入参数的嘞
    runMinecraft(minecraftVersion:str,Username:str):
    '''
    options = minecraft_launcher_lib.utils.generate_test_options()
    if userName != None:
        options['username'] = userName
    print(options)
    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(minecraftVersion, minecraft_directory, options)
    print(minecraft_command)
    minecraftVersion = float(minecraftVersion[2:])
    print(minecraftVersion)
    try:
        if int(minecraftVersion) >= 20:
            minecraft_command.remove('--quickPlaySingleplayer')
            minecraft_command.remove('--quickPlayMultiplayer')
            minecraft_command.remove('--quickPlayRealms')
    except:
        pass
    print(minecraft_command)
    subprocess.run(minecraft_command)

def downloadMinecraft(mcVersion:str):
    status = downloadVersion(mcVersion,minecraft_directory)
    if status == "error":
        downloadMinecraftSlowly(mcVersion)

def downloadMinecraftSlowly(mcVersion:str):
    minecraft_launcher_lib.install.install_minecraft_version(mcVersion, minecraft_directory,callback=callback)

def microsoftLogin():
    #minecraft_launcher_lib.microsoft_account.get_login_url(client_id: str, redirect_uri: str
    url = minecraft_launcher_lib.microsoft_account.get_login_url("a72d2234-2525-4c00-b8b8-d2bf6ba09d13","https://login.live.com/oauth20_desktop.srf")
    webbrowser.open(url)

print("设备信息说明\n======================\n操作系统",myOS,"\n默认mc地址",minecraft_directory,"\n======================")

# installNeoForge("1.20.1",)
# downloadMinecraft("1.20.1")

installFabric("1.20.1",minecraft_directory)

# else:
#     print('操作系统不匹配，请检查后再试')
#     exit()
