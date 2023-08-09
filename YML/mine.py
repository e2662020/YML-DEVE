#导入库文件
import minecraft_launcher_lib
from downloadMC import downloadVersion
from downloadForge import installForge
import subprocess
import os
import platform
from logging import *

#设置变量
minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()
myPATH = os.getcwd()
mcDir = minecraft_directory + "/versions/"
myOS = platform.system()
# if myOS == "Windows":
def set_status(status: str):
    print(status)


def set_progress(progress: int):
    if current_max != 0:
        print(f"{progress}/{current_max}")


def set_max(new_max: int):
    global current_max
    current_max = new_max

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
print("设备信息说明\n======================\n操作系统",myOS,"\n默认mc地址",minecraft_directory,"\n======================")

# else:
#     print('操作系统不匹配，请检查后再试')