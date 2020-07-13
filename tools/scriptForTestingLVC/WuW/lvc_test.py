import time
import subprocess
from datetime import datetime
# pip install pygame
from pygame import mixer
from ppadb.client import Client as AdbClient
from selenium import webdriver
import os

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

    apksInstall = [apk_instal1]
    for device in devices:
        for apk in apksInstall:
            print("installing " + apk)
            device.install(apk)
    print("installing Done")      
    time.sleep(1)
    
    # grant perimissions
    # Ref: http://developer.android.com/reference/android/Manifest.permission.html
    adbLoc = "/Users/xxxxxx/Library/Android/sdk/platform-tools/adb "
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
    subprocess.call("adb shell monkey -p com.amazon.sampleapp  -c android.intent.category.LAUNCHER 1",shell=True)
    time.sleep(10)
    # these numbers only work on the Samsung Sm-T720 tablet
    # touch the menu button
    
    # you can get these numbers by enabling the Pointer Location tab under Developer Tools
    subprocess.call("adb shell input tap 1528 72", shell=True)  
    
    # touch the Login with Amazoon button
    subprocess.call("adb shell input tap 1250 225", shell=True)  
    time.sleep(5)
    
    # get the 5 digit number
    # get logcat
    subprocess.call("adb logcat -d > logcat.txt", shell=True)        
    # search for results
    feed =  open("logcat.txt", encoding = "ISO-8859-1")
    while True:
        line = feed.readline()
        if line.find("url=https://amazon.com/us/code") != -1:
            code = line[-7:-1]
            # clear logcat
            subprocess.call("adb logcat -b all -c", shell=True)    
            break
    
    print(code)
    # enter code into: https://amazon.com/us/code
    
    
    browser = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
    browser.get("https://www.amazon.com/a/code?language=en_US")
    
    email_input = browser.find_element_by_id("ap_email")
    email_input.send_keys("email@hotmail.com") # enter log in email here
    
    pass_input = browser.find_element_by_id("ap_password")
    pass_input.send_keys("email_password") # enter log in password here
    
    signin_button = browser.find_element_by_id("signInSubmit")
    signin_button.click()
    
    register_input = browser.find_element_by_id("cbl-registration-field")
    register_input.send_keys(code)
    
    continue_button = browser.find_element_by_id("cbl-continue-button")
    continue_button.click()
    
    browser.close()
    
    
    mixer.init()
    mixer.music.load('speech_20200711011839791.mp3')
       
    
    # wait for engine to load
    time.sleep(10)
    
    
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