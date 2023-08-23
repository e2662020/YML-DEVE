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
import psutil


#下载版本

#设置变量
minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()
myPATH = os.getcwd()
mcDir = minecraft_directory + "/versions/"
myOS = platform.system()
with open(myPATH+"azureAPI.txt", "r") as f:
    azureApiKey = f.read
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

def runMinecraft(minecraftVersion:str,ram = None,userName:str = None):
    '''
    没啥说的，输入参数的嘞
    runMinecraft(minecraftVersion:str,Username:str):
    '''
    options = minecraft_launcher_lib.utils.generate_test_options()
    if userName != None:
        options['username'] = userName
    if ram != None:
        options["jvmArguments"] = ["-Xmx"+str(ram)+"M", "-Xms0M"]
    print(options)
    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(minecraftVersion, minecraft_directory, options)
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

def getRAM():
    # 获取信息(没必要的代码，仅示范，可删去)
    mem = psutil.virtual_memory()
    mem_total = round(mem.total / 1024 / 1024 / 1024, 2)
    mem_total1 = round(mem.total / 1024 / 1024, 2)
    system = f"RAM:\n内存使用率:{mem.percent}%\n物理内存总量:{mem_total}GB={mem_total1}MB\n"
    mem_available = round(mem.available / 1024 / 1024 / 1024, 2)
    mem_availablem1 = round(mem.available / 1024 / 1024, 2)
    system += f"可用内存:{mem_available}GB={mem_availablem1}MB\n"
    mem_used = round(mem.used / 1024 / 1024 / 1024, 2)
    mem_used1 = round(mem.used / 1024 / 1024, 2)
    system += f"已用内存:{mem_used}GB={mem_used1}MB\n"
    mem_free = round(mem.free / 1024 / 1024 / 1024, 2)
    mem_free1 = round(mem.free / 1024 / 1024, 2)
    system += f"空闲内存:{mem_free}GB={mem_free1}MB\n"
    print(system)
    # 计算最优内存占用
    ram_use = int(round(psutil.virtual_memory().free / 1024 / 1024, 2) / 10 * 8)  # 乘以8意思是取可用内存的80%
    if ram_use > 1024 * 3:  # 乘以3意思是3GB，动态获取不超过这个值
        ram_use = 1024 * 3
    print(ram_use)
    return ram_use



print("设备信息说明\n======================\n操作系统",myOS,"\n默认mc地址",minecraft_directory,"\n======================")

# downloadMinecraft("1.20.1")
ramMAX = getRAM()
if ramMAX <= 1024:
    while True:
        a = input("你的剩余内存小于1G，游玩体验会有限制，确认是否启动？[y/n]")
        if a == "y" or a == "Y":
            runMinecraft("1.20.1",ramMAX,"RATE")
            break
        elif a=="n" or a=="N":
            quit(0)
        else:
            print("我看不懂，请再输入一遍")
# installFabric("1.20.1",minecraft_directory)

# else:
#     print('操作系统不匹配，请检查后再试')
#     exit()
