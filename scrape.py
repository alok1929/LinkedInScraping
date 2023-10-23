from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import re
import pandas as pd
import matplotlib.pyplot as plt
from openpyxl import Workbook, load_workbook

username_string = 'alokhegde221@gmail.com'
password_string = 'Gr37gj3fcmEpt9'
link_username = 'knightofsteel'

webdriver_path = '/usr/bin/chromedriver'  # Path to the Chrome WebDriver executable

# Set up the Chrome WebDriver instance in headless mode
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome()

# Enter the specified information to login to LinkedIn:
driver.get('https://www.linkedin.com/login')
elementID = driver.find_element(By.ID, 'username')
elementID.send_keys(username_string)
elementID = driver.find_element(By.ID, 'password')
elementID.send_keys(password_string)
elementID.submit()

# Wait for the login process to complete
time.sleep(15)

# Open the recent post activity page of the LinkedIn user you specified:
recent_activity_link = f"https://www.linkedin.com/in/{link_username}/detail/recent-activity/all/"
driver.get(recent_activity_link)

# Wait for the page to load
time.sleep(3)

# Get the page source and create a BeautifulSoup object
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

# Calculate the number of scrolls depending on the input
number_of_posts = 125 # Set the desired number of posts
number_of_scrolls = (number_of_posts - 5) // 5
print(number_of_scrolls)
likes = []

SCROLL_PAUSE_TIME = 5

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

for scroll in range(number_of_scrolls):
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)
    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height


# Query the contents
src = driver.page_source
soup = BeautifulSoup(src, features="lxml")

# Find likes on LinkedIn
# Open the existing workbook or create a new one
workbook=Workbook()
sheet = workbook.active

likes_bs4tags = soup.find_all("span", attrs={"class": "social-details-social-counts__reactions-count"})

for i, tag in enumerate(likes_bs4tags, start=1):
    strtag = str(tag)
    list_of_matches = re.findall('[,0-9]+', strtag)
    last_string = list_of_matches.pop()
    print(last_string)
    k='A'+str(i)
    sheet['A1']="NUMBER OF LIKES"
    sheet[k] = last_string

# Find comments on LinkedIn
comments_bs4tags = soup.find_all("li", attrs={"class": "social-details-social-counts__comments"})
comments_data = []

for o,tag in enumerate(comments_bs4tags,start=1):
    strtag = str(tag)
    list_of_matches = re.findall(r'\b\d+\b', strtag)
    if list_of_matches:
        last_string = list_of_matches[-1]
        comments_data.append(int(last_string))
    print(last_string)
    kc='B'+str(o)
    sheet['B1']="NUMBER OF COMMENTS"
    sheet[kc] = last_string

# Save the workbook
workbook.save('inpu.xlsx')

