import time
import os
import subprocess
from datetime import datetime
# pip install pygame
from pygame import mixer
from ppadb.client import Client as AdbClient

# Default is "127.0.0.1" and 5037
client = AdbClient(host="127.0.0.1", port=5037)
devices = client.devices()
TestCounter = 1


while TestCounter < 250:
    apk_delete1 = "com.amazon.sampleapp"
    apk_delete2 = "com.amazon.alexalve"
    apk_delete3 = "com.amazon.lvc.lm.en_US"
    apksDelete = [apk_delete1, apk_delete2, apk_delete3]
    for device in devices:
        for apk in apksDelete:
            print("uninstalling " + apk)
            device.uninstall(apk)
    print("uinstalling Done")
    time.sleep(1)
    
    
    apk_instal1 = "app-local-release-AlignedSigned.apk"
    apk_instal2 = "lmapp-en_US-release-AlignedSigned.apk"
    apk_instal3 = "lveapp-release-AllignedSigned.apk"
    apksInstall = [apk_instal1, apk_instal2, apk_instal3]
    for device in devices:
        for apk in apksInstall:
            print("installing " + apk)
            device.install(apk)
    print("installing Done")      
    time.sleep(1)
    
    # grant perimissions
    # Ref: http://developer.android.com/reference/android/Manifest.permission.html
    adbLoc = "/Users/xxxxx/Library/Android/sdk/platform-tools/adb "
    perimission1 = "shell pm grant com.amazon.sampleapp android.permission.RECORD_AUDIO"
    perimission2 = "shell pm grant com.amazon.sampleapp android.permission.READ_EXTERNAL_STORAGE"
    perimission3 = "shell pm grant com.amazon.sampleapp android.permission.WRITE_EXTERNAL_STORAGE"
    perimission4 = "shell pm grant com.amazon.sampleapp android.permission.ACCESS_FINE_LOCATION"
    perimission5 = "shell pm grant com.amazon.sampleapp android.permission.READ_EXTERNAL_STORAGE"
    perimission6 = "shell pm grant com.amazon.sampleapp android.permission.ACCESS_FINE_LOCATION"
    perimission7 = "shell pm grant com.amazon.sampleapp android.permission.ACCESS_COARSE_LOCATION"
    permission = [perimission1, perimission2, perimission3, perimission4, perimission5, perimission6, perimission7]
    for x in permission:
        subprocess.call(adbLoc + x, shell=True)
    print("Perimissions Done")   

    # clear logcat
    subprocess.call("adb logcat -b all -c", shell=True)    
    
    
    # lanuch the app
    subprocess.call("adb shell monkey -p com.amazon.sampleapp  -v 500",shell=True)
    
    mixer.init()
    mixer.music.load('speech_20200711011839791.mp3')
   
    
    # wait for LVC to load
    time.sleep(35)
    

    # pygame  mixer is flaky  
    # try 10 times to play the command if after 10 times it fails, log the results and continue
    soundCount = 0
    while soundCount < 10:
        
        mixer.music.play()
        # play the command
        time.sleep(10)
    
        # get log cat
        subprocess.call("adb logcat -d > logcat.txt", shell=True)        
        # search for results
        eventCount = 0
        feed =  open("logcat.txt", encoding = "ISO-8859-1")
        while True:
            line = feed.readline()
            if not line: break
            elif line.find("CarControl:PowerController,endpoint=ac,name=TurnOn") != -1:
                eventCount += 1
                break
        if eventCount == 0:
            soundCount += 1
        else:
            break
            
    if soundCount == 10: # problem found: Store the log
        print("Problem Found")
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S") + ".txt"
        feed =  open("logcat.txt", encoding = "ISO-8859-1")
        while True:
            line = feed.readline()
            if not line: break
            with open(current_time, "a") as f1:
                f1.write(line)
        # store results in a text file
        with open('testResults.txt', 'a') as writer:
            writer.write("Test Number: " + str(TestCounter) + " :: " + "FAIL")
            writer.write("\n")
    else:
        # store results in a text file
        with open('testResults.txt', 'a') as writer:
            writer.write("Test Number: " + str(TestCounter) + " :: " + "GOOD")
            writer.write("\n")
        

    # kill app
    subprocess.call("adb shell am force-stop com.amazon.sampleapp -v 500", shell = True)
    time.sleep(1)
    
    TestCounter += 1

os.delete("logcat.txt")