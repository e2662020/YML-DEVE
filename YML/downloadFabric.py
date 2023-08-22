import os

def installFabric(mcversion,mcDir):
    path = os.getcwd()
    path = path+"/fabricInstaller"
    os.system('java -jar fabricInstaller.jar client -snapshot -dir "'+mcDir+'" -mcversion "'+mcversion+'')