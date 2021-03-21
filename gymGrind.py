import selenium
import time
import datetime
import tkinter as tk
import tkinter.font as font
from threading import Thread
import sys
from tkinter import *
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
day = datetime.datetime.today().weekday()


def logInToPage(u, p, t):
    global driver
    driver = webdriver.Chrome()
    driver.get("https://rec.carleton.ca/Program/GetProducts?classification=d17305dd-be9c-4889-a554-336cb4fb78e0&category=38f6aaac-d0bd-448c-9069-6523b8bb73d9")
    #press Log In
    logIn1 = driver.find_element_by_id("loginLink")
    logIn1.click()
    time.sleep(.5)
    #pop up "LOGIN WITH MC1 CREDENTIALS"
    logIn2 = driver.find_element_by_css_selector('.btn-soundcloud')
    logIn2.click()

    #enter username and password
    userBox = driver.find_element_by_id("userNameInput")
    userBox.send_keys(u)
    passBox = driver.find_element_by_id("passwordInput")
    passBox.send_keys(p)

    #login
    loginButton = driver.find_element_by_id("submitButton")
    loginButton.click()
    if(len(driver.find_elements_by_id("errorText")) <= 0):
        selectDay(day, t)
    else:
        driver.quit()
        time.sleep(3)
        screen.mainloop()        

def selectDay(d, t):
    time.sleep(.25)
    if driver.find_element_by_id("gdpr-cookie-accept"):
        cookiesBtn = driver.find_element_by_id("gdpr-cookie-accept")
        cookiesBtn.click()
    #monday = 0, tues = 1 etc.
    switcher = {
        0: 4,
        1: 0,
        2: 2,
        3: 3,
        4: 1,
        5: 5,
        6: 6
    }
    dayOfWeekBtn = driver.find_elements_by_css_selector(".TitleText-SP")[switcher.get(day)]
    dayOfWeekBtn.click()
    finishRegistration(t)

def finishRegistration(t):
    refresh(t)
    timeBtn = driver.find_elements_by_css_selector(".btn-primary")
    numTimes = len(timeBtn)-3
    if numTimes >= 0:
        newBtn = timeBtn[numTimes]
        actions = ActionChains(driver)
        actions.move_to_element(newBtn)
        actions.perform()
        newBtn.click()
    else:
        exit()
    
    # registerBtn = driver.find_element_by_css_selector(".disableOnChoice")
    # driver.execute_script("return arguments[0].scrollIntoView();", registerBtn)
    # registerBtn.click()

    #scroll and click accept
    time.sleep(.5)
    acceptBtn = driver.find_element_by_css_selector("#btnAccept")
    actions = ActionChains(driver)
    actions.move_to_element(acceptBtn)
    actions.perform()
    acceptBtn.click()
    
    continueBtn = driver.find_elements_by_css_selector(".btn-primary")[4]

    continueBtn.click()

    radios = driver.find_elements_by_id("rbtnYes")
    for i in radios:
        i.click()
    

    addToCart = driver.find_elements_by_css_selector(".btn-primary")[3]
    actions = ActionChains(driver)
    actions.move_to_element(acceptBtn)
    addToCart.click()

    checkout = driver.find_element_by_id("checkoutButton")
    checkout.click()

    # for i in range(0,5):
    #     print(driver.find_elements_by_css_selector(".btn-primary")[i].get_attribute("onclick"))
    time.sleep(.5)
    checkoutConfirm = driver.find_elements_by_css_selector(".btn-primary")[4].click()

    time.sleep(5)

def refresh(t):
    mySleep(t)
    time.sleep(2)
    driver.refresh()

def runIt():
    myUsername = username.get()
    myPassword = password.get()
    myTime = timeOptions.get()
    switcher = {
        "6:00-6:45":6,"7:00-7:45":7,"8:00-8:45":8,"9:00-9:45":9,"10:00-10:45":10,"11:00-11:45":11,"12:00-12:45":12,"1:00-1:45*":13,"2:00-2:45*":14,"3:00-3:45*":15,"4:00-4:45*":16,"5:00-5:45*":17,"6:00-6:45*":18,"7:00-7:45*":19,"8:00-8:45*":20,"9:00-9:45*":21
    }
    seconds = switcher.get(myTime)*3600
    now = datetime.datetime.now()
    secondsSinceMidnight = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
    screen.destroy()
    timeLeft = convert(seconds-secondsSinceMidnight)
    
    print("Bot will launch in ",timeLeft,"Please leave this terminal open.")
    if(seconds-secondsSinceMidnight>300):
        mySleep(seconds-300)
    logInToPage(myUsername, myPassword, seconds)

def mySleep(t):
    now = datetime.datetime.now()
    secondsSinceMidnight = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
    if(t-secondsSinceMidnight > 0):
        time.sleep(t-secondsSinceMidnight)

def convert(seconds): 
    seconds = seconds % (24 * 3600) 
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return "%d:%02d:%02d." % (hour, minutes, seconds) 


screen = tk.Tk()
screen.geometry("500x500")
screen.title("TheHills Gym Bot")
heading = Label(text = "TheHills Gym Bot", bg = "grey", fg = "black", width = "500", height = "3")
heading.config(font=("Arial",13))
heading.pack()

usernameTxt = Label(text = "Username: ",)
passwordTxt = Label(text = "Password: ",)
timeTxt = Label(text = "Time: ",)
errorTxt = Label(text = "",)
usernameTxt.place(x=15,y=70)
passwordTxt.place(x=15,y=140)
timeTxt.place(x=15,y=210)
errorTxt.place(x=15, y=320)
username = StringVar()
password = StringVar()
n = tk.StringVar() 
timeOptions = ttk.Combobox(screen, width = 27, textvariable = n) 
timeOptions['values'] = ["6:00-6:45","7:00-7:45","8:00-8:45","9:00-9:45","10:00-10:45","11:00-11:45","12:00-12:45","1:00-1:45*","2:00-2:45*","3:00-3:45*","4:00-4:45*","5:00-5:45*","6:00-6:45*","7:00-7:45*","8:00-8:45*","9:00-9:45*"]

timeOptions.current() 

usernameEntry = Entry(textvariable = username, width = "30")
passwordEntry = Entry(textvariable = password, width = "30")
usernameEntry.place(x=15, y = 100)
passwordEntry.place(x=15, y = 170)
timeOptions.place(x=15, y= 240)
submit = Button(screen, text = "Submit", width = "30", height = "2", command = runIt, bg = "grey")
submit.place(x="15",y=270)

screen.mainloop()
