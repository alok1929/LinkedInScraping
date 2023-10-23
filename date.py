from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import re
from openpyxl import Workbook

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
time.sleep(5)

# Calculate the date range (from now to a year ago)
end_date = datetime.now()
start_date = end_date - timedelta(days=365)

likes = []

# Loop over each month within the year
while start_date <= end_date:
    # Convert the date range to LinkedIn's format
    end_date_str = end_date.strftime("%Y-%m-%d")
    start_date_str = start_date.strftime("%Y-%m-%d")

    # Open the recent post activity page of the LinkedIn user for the current month
    recent_activity_link = f"https://www.linkedin.com/in/{link_username}/detail/recent-activity/shares/?dateRange={start_date_str}:{end_date_str}"
    driver.get(recent_activity_link)

    # Wait for the page to load
    time.sleep(3)

    # Get the page source and create a BeautifulSoup object
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # Calculate the number of scrolls depending on the input
    number_of_posts = 20  # Set the desired number of posts
    number_of_scrolls = (number_of_posts - 5) // 5
    print(number_of_scrolls)

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

    # Get the page source after scrolling and create a BeautifulSoup object
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find likes on LinkedIn
    likes_bs4tags = soup.find_all("span", attrs={"class": "social-details-social-counts__reactions-count"})

    for tag in likes_bs4tags:
        likes_str = tag.get_text(strip=True)
        likes_count = int(likes_str.replace(",", ""))
        likes.append(likes_count)

    # Move to the previous month
    end_date = start_date - timedelta(days=1)
    start_date = end_date - timedelta(days=365)

# Reverse the list to get the likes in chronological order
likes.reverse()

print(likes)