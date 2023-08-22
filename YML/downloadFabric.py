import os

def installFabric(mcversion,mcDir):
    path = os.getcwd()
    path = path+"/fabricInstaller"
    command = 'java -jar fabricInstaller.jar client -snapshot -dir "' + mcDir + '" -mcversion "' + mcversion + '"'
    print(command)
    os.system(command)