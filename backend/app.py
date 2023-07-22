import time
import json
import random

import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
# nosuchelementexception
# from selenium.common.exceptions import NoSuchElementException

import os
import openai

from flask import Flask, request, jsonify
import random
from flask_cors import CORS
import threading

app = Flask(__name__)
CORS(app)

openai.api_key = 'OPENAI API KEY'

ACCOUNTS = [
    {"email": "GOOGLE EMAIL", "password": "PASSWORD",
        "recovery": "RECOVERY EMAIL"},

    # add as many accounts as you like
]

def login_to_google_account(driver, account):
    email = account["email"]
    password = account["password"]
    recovery = account["recovery"]

    driver.get(
        "https://twitter.com/i/flow/login")
    time.sleep(15)
    # Explicit wait for the button to be clickable
    try:
        # make action chain that tabs and then presses enter
        actions = ActionChains(driver)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.ENTER)
        actions.perform()
    except Exception as e:
        print(e)
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(2)

    driver.find_element(
        By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input").send_keys(email)
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[2]/div/div[1]/div/div/button").click()

    time.sleep(5)

    driver.find_element(
        By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[1]/div/form/span/section[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input").send_keys(password)
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[2]/div/div[1]/div/div/button").click()

    time.sleep(5)
    # screnshot 1
    # full_screenshot(driver, "1")
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div/c-wiz/div/div/div/div[2]/div[4]/div[1]/button"))).click()
    except:
        print("The element was not found.")

    time.sleep(5)
    # CONFIRM TO ALLOW TWITTER
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="confirm_yes"]'))).click()
        time.sleep(5)
        driver.switch_to.window(driver.window_handles[-1])
        # make an action chain for typing 'j' and then tab and then '1' and then tab and then '1990' and then tab and then 'enter'
        actions = ActionChains(driver)
        actions.send_keys("j")
        actions.send_keys(Keys.TAB)
        actions.send_keys("1")
        actions.send_keys(Keys.TAB)
        actions.send_keys("1990")
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.ENTER)
        actions.perform()

        time.sleep(5)

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div'))).click()
        time.sleep(5)

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div'))).click()
        time.sleep(5)

        driver.switch_to.window(driver.window_handles[-1])
    except:
        print("The element was not found.")
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div/div[1]/div/div/main/div[4]/div[1]"))).click()
    except:
        print("The second element was not found.")

    try:
        driver.find_element(
            By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div/ul/li[3]/div").click()
        time.sleep(10)
        # full_screenshot(driver, "2")
        try:

            driver.find_element(
                By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[2]/div[1]/div/div[1]/div/div[1]/input").send_keys(recovery)

        except:

            print("The recovery input was not found.")
        # full_screenshot(driver, "3")
        driver.find_element(
            By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button").click()

    except:
        print("The third element was not found.")

    time.sleep(5)
    print('Logged in to Google account.')

def find_tweet(driver, tweet_url):
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(2)
    driver.get(tweet_url)
    time.sleep(15)
    print('Found tweet.')

    tweet_text = driver.find_element(
        By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div/div/div[1]/div/div/article').text

    review_instruction = f"Reply to the tweet that the user provides in an extremely rude way. Max 250 characters."

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": review_instruction},
            {"role": "user", "content": tweet_text}
        ]
    )

    reply = response['choices'][0]['message']['content']
    print(reply)

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div/div/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div[1]/div/div/div/div/div/label/div[1]/div/div/div/div/div/div[2]/div')))
        reply_box = driver.find_element(
            By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div/div/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div[1]/div/div/div/div/div/label/div[1]/div/div/div/div/div/div[2]/div')
        reply_box.click()
        reply_box.send_keys(reply)
        time.sleep(2)
        # make a action chain of 4 tabs, and then enter
        ActionChains(driver).send_keys(
            Keys.TAB * 4).send_keys(Keys.ENTER).perform()
        time.sleep(15)
    except:
        print("Reply box not found.")

@app.route("/tweet_process", methods=['POST'])
def tweet_process():
    if request.method == 'POST':
        tweet_url = request.json['tweet_url']
        
        if tweet_url is None or tweet_url == "":
            return jsonify({'message': 'Tweet URL is required'}), 400

        account = random.choice(ACCOUNTS)

        chrome_options = uc.ChromeOptions()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--profile-directory=Default")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--disable-plugins-discovery")
        chrome_options.add_argument("--incognito")
        # chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument(
            "user_agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

        driver = uc.Chrome(options=chrome_options)
        driver.delete_all_cookies()
        
        login_to_google_account(driver, account)
        thread = threading.Thread(target=find_tweet, args=(driver, tweet_url,))
        thread.start()
        return jsonify({'message': 'Processing started for tweet'}), 202

if __name__ == '__main__':
    app.run(port=5000)
