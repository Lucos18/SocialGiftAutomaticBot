from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from instagrapi import Client

import json
import os
import warnings

#Default list of Counter that will be added to the file "Counter.json" when the file doesn't not exists.
listLikeFollowStories = [{"Like" : 0, "Follow" : 0, "Stories" : 0}]

#Default list of Settings that will be added to the file "Settings.json" when the file doesn't not exists.
listSettings = {"like" : False, "follow" : False, "comments" : True, "stories" : False, "video" : False, "directoryChromeSettings": "C:\\Users\\YourPCUsername\\AppData\\Local\\Google\\Chrome\\User Data"}

#It will check if the file "dump.json" exists in the directory, if not it will create one after the login to the instagram account.
#The dump file will contain all the information of the "device" used to login on instagram, so there is a less risk to get the account blocked.
def checkDumpFile():
    if (os.path.exists("dumps.json")):
        cl.load_settings('dumps.json')
        cl.login(data["accountUsername"], data["accountPassword"])
        cl.get_timeline_feed()
    else:
        cl.login(data["accountUsername"], data["accountPassword"])
        cl.dump_settings('dumps.json')
        print("dump file not found, i have created one for you.")

#Will get the Counter list as parameter and write inside the "Counter.json" file.
def writeListInformation(listCounter):
    CounterCC = open("Counter.json","w")
    json.dump(listCounter, CounterCC)
    CounterCC.close()

#If video campaign is found it will wait 10 minutes and then it will press "Conferma" button
def watchVideoWait():
    print("video found, i will wait 600 seconds, if you want to disable this and skip it please configure the settings.json file.")
    sleep(600)
    driver.find_element_by_xpath(('//button[contains(text(),"CONFERMA")]')).click();

#If follow campaign is found it will do the follow on instagram by getting the username and using different api request.
def follow_instagram():
    try:
        global followCounter
        #It will get the link to the instagram profile inside the telegram message
        link_instagram = driver.find_element_by_class_name("anchor-url").get_attribute('href')
        #Then it will split the link in multiple parts
        username_instagram = link_instagram.split("/")
        #After the split, i will specifically say to get only the username of the account from instagram link, and then from that i will get the userid
        userid = cl.user_id_from_username(username_instagram[3])

        #True if the follow went successfully, False if the account is blocked for many follow in an hour or the profile doesn't exists.
        if(cl.user_follow(userid)):
            print("Follow done at the link: " + link_instagram)
            driver.find_element_by_xpath(('//button[contains(text(),"CONFERMA")]')).click();
            followCounter = followCounter + 1
        else:
            print("The profile doesn't exist at the link: " + link_instagram)
            driver.find_element_by_xpath(('//button[contains(text(),"SALTA")]')).click();
    except:
        print("Follow not done at the link: " + link_instagram)
        print("It is possible that your account has been blocked from instagram or the account is private, in any case i will wait 2 minutes before retry")
        sleep(120)

#It will check if the campaign is an AD, if true it will skip it.
def controllo_campagna():
    try:
        driver.find_element_by_xpath(('//button[contains(text()," NON MI INTERESSA ")]')).click();
        print("It is a campaign link, i will skip it.")
        return False
    except:
        try:
            driver.find_element_by_xpath(('//div[contains(.," Solo per ")]'));
            driver.find_element_by_xpath(('//button[contains(text(),"SALTA")]')).click();
            print("It is a campaign link, i will skip it.")
            return False
        except:
            print("campaign link not found, i will continue to the next one.")
            return True

#If Like campaign is found it will do the Like action on instagram by getting the link and using different api request.
def actionLike():
    try:
        global likeCounter 
        #It will get the link to the instagram profile inside the telegram message
        link_instagram = driver.find_element_by_class_name("anchor-url").get_attribute('href')
        #It will get the "mediapk" from the link
        mediapk = cl.media_pk_from_url(link_instagram)
        #Then with the "mediapk" we can get the mediaid to do the Like action
        mediaid = cl.media_id(mediapk)

        #True if Like went successfully, false if the post doesn't exists
        if(cl.media_like(mediaid)):
            try:
                print('Like done at the link:' + link_instagram)
                driver.find_element_by_xpath(('//button[contains(text(),"CONFERMA")]')).click();
                likeCounter = likeCounter + 1
                sleep(3)
            except:
                return
        else:
            print("Photo doesn't exist, i will skip to the next campaign.")
            driver.find_element_by_xpath(('//button[contains(text(),"SALTA")]')).click();
            sleep(3)
    except:
        print("Photo doesn't exist, i will skip to the next campaign. Error link:" + link_instagram)
        driver.find_element_by_xpath(('//button[contains(text(),"SALTA")]')).click();
        sleep(3)

#If comment campaign is found, at the moment it will only skip it
def skipComments():
    print('I will skip the comments.')
    driver.find_element_by_xpath(('//button[contains(text(),"SALTA")]')).click();
    sleep(3)

#If story campaign is found, it will wait 30 seconds before continuing.
def confirmStories():
    global storiesCounter
    print('Story found, I will wait 30 seconds before pressing "Conferma".')
    sleep(30)
    driver.find_element_by_xpath(('//button[contains(text(),"CONFERMA")]')).click();
    storiesCounter = storiesCounter + 1
    sleep(3)

#Will read the login credentials, please set them right i don't know what happens when it's wrong 
def loginCredentialsFileRead():
    global data
    pathCredentials = r"loginCredentials.json"
    try:
        assert os.path.isfile(pathCredentials)
        with open(pathCredentials, "r") as f:
            data = json.load(f)
            f.close()
    except:
        print("Error! Account credentials not found, wrong path or no administration privileges.")

#Will read the counter file, and if not found it will create a new one with default values
def counterFileRead():
    global listCounter
    pathCounter = r"Counter.json"
    try:
        assert os.path.isfile(pathCounter)
        with open(pathCounter, "r") as c:
            listCounter = json.load(c)
            c.close()
    except:
        print("Warning! Counter file not found, creating a new one.")
        with open('Counter.json', 'w') as counterC:
            print("The json file Counter has been created.")
            json.dump(listLikeFollowStories, counterC)
            print("The file Counter is used to store how many Likes/Follow/Stories the bot did, so relax and watch!")
            counterC.close()
        with open(pathCounter, "r") as c:
            listCounter = json.load(c)
            c.close()

#Will read the Settings file, and if not found it will create a new one with default values
def settingsFileRead():
    global listSettings
    pathSettings = r"Settings.json"
    try:
        assert os.path.isfile(pathSettings)
        with open(pathSettings, "r") as s:
            listSettings = json.load(s)
            print("The file Settings has been loaded.")
    except:
        print("Warning! Settings file not found, creating a new one with default values.")
        with open('Settings.json', 'w') as Settings:
            print("The json file Settings has been created.")
            json.dump(listSettings, Settings)

#Disable warnings created by old deprecated commands that i will replace later on
warnings.filterwarnings("ignore")
finishedCampaigns = False
loginCredentialsFileRead()
counterFileRead()
settingsFileRead()
print("Creating Chromedriver client.")
print("Trying to login into instagram account.")
#Creating Chromedriver Client
cl = Client()
checkDumpFile()
print("Login successfull!")
chrome_options = Options()
chrome_options.add_argument('user-data-dir=' + listSettings["directoryChromeSettings"])
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(5)
#Get the list of Counter from "counter.json" file that stores counters of past sessions.
likeCounter = listCounter[0]["Like"]
followCounter = listCounter[0]["Follow"]
storiesCounter = listCounter[0]["Stories"]
print("Opening socialgiftbot webpage.")
print("like settings: " + str(listSettings["like"]))
print("follow settings: " + str(listSettings["follow"]))
print("stories settings: " + str(listSettings["stories"]))
print("video settings: " + str(listSettings["video"]))
#Opening the website of the bot
driver.get("https://web.telegram.org/k/#@socialgiftbot")

while not (finishedCampaigns):
    likeNotFound = listSettings["like"]
    followNotFound = listSettings["follow"] 
    commentNotFound = listSettings["comments"] 
    storiesNotFound = listSettings["stories"] 
    videoNotFound = listSettings["video"]
    campaignNotFound = False
    while not (campaignNotFound):
        sleep(3)
        campaignNotFound = controllo_campagna()
        sleep(3)
    try:
        while not (likeNotFound):
            sleep(3)
            driver.find_element(By.XPATH, '//div[@class="message"]//img[@alt="❤️"]')
            actionLike()
            listCounter = [{"Like" : likeCounter, "Follow" : followCounter, "Stories" : storiesCounter}]
            writeListInformation(listCounter)
            sleep(3)
    except:
        print("Like not found, i will continue.")
        likeNotFound = True
    try:
        #will added later on
        while not (commentNotFound):
            driver.find_element(By.XPATH, '//div[@class="message"]//img[@alt="💬"]')
            skipComments()
    except:
        print("Comment not implemented, i will skip it.")
        commentNotFound = True
    try:
        while not (storiesNotFound):
            driver.find_element(By.XPATH, '//div[@class="message"]//img[@alt="👁️"]')
            confirmStories()
            listCounter = [{"Like" : likeCounter, "Follow" : followCounter, "Stories" : storiesCounter}]
            writeListInformation(listCounter)
    except:
        print("Story not found, i will continue.")
        storiesNotFound = True
    try:
        while not (videoNotFound):
            #mmmm videos
            driver.find_element(By.XPATH, '//strong[normalize-space()="Per Intero"]')
            watchVideoWait()
    except:
        print("Video not found, i will continue.")
    try:
        while not (followNotFound):
            sleep(5)
            driver.find_element(By.XPATH, '//div[@class="message"]//img[@alt="💎"]')
            follow_instagram()
            listCounter = [{"Like" : likeCounter, "Follow" : followCounter, "Stories" : storiesCounter}]
            writeListInformation(listCounter)
            sleep(5)
    except:
        print("Follow text not found, i will continue to the next one.")
        followNotFound = True
    try:
        driver.find_element(By.XPATH, '//img[@alt="⏳"]')
        finishedCampaigns = True
        print("Found finished campaign message, i will stop the bot.")
    except:
        sleep(1)
    


