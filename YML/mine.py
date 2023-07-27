#导入库文件
import minecraft_launcher_lib
from download import download
import subprocess

#设置变量
minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()
def runMinecraft(minecraftVersion:str,userName:str):
    '''
    没啥说的，输入参数的嘞
    runMinecraft(minecraftVersion:str,Username:str):
    '''
    options = minecraft_launcher_lib.utils.generate_test_options()
    options['username'] = userName
    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(minecraftVersion, minecraft_directory, options)
    subprocess.run(minecraft_command)

