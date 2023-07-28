#导入库文件
import minecraft_launcher_lib
from download import downloadVersion
import subprocess
import os
import requests

#设置变量
minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()
myPATH = os.getcwd()
mcDir = minecraft_directory + "/versions/"

headers = {
'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.183'
}

def runMinecraft(minecraftVersion:str,userName:str):
    '''
    没啥说的，输入参数的嘞
    runMinecraft(minecraftVersion:str,Username:str):
    '''
    options = minecraft_launcher_lib.utils.generate_test_options()
    options['username'] = userName
    print(options)
    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(minecraftVersion, minecraft_directory, options)
    minecraftVersion = float(minecraftVersion[2:])
    print(minecraftVersion)
    if int(minecraftVersion) >= 20:
        minecraft_command.remove('--quickPlaySingleplayer')
        minecraft_command.remove('--quickPlayMultiplayer')
        minecraft_command.remove('--quickPlayRealms')
    print(minecraft_command)
    subprocess.run(minecraft_command)

def downloadMinecraft(mcVersion:str):
    downloadVersion(mcVersion,minecraft_directory)

runMinecraft("1.20.1","RATE")