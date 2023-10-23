from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

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

print("done")
# Wait for the login process to complete
time.sleep(5)

# Calculate the date range for the desired month
end_date = datetime(2023, 5, 31)  # Specify the end date of the desired month
start_date = datetime(2023, 5, 1)  # Specify the start date of the desired month

# Open the LinkedIn profile page of the specified user
profile_link = f"https://www.linkedin.com/in/{link_username}"
driver.get(profile_link)
print("done")

# Click on the "Activity" tab
activity_tab = driver.find_element(By.LINK_TEXT, 'Activity')
activity_tab.click()

# Wait for the page to load
time.sleep(5)

# Get the page source
page_source = driver.page_source

# Find the section containing the posts
posts_section = driver.find_element(By.XPATH, "//section[contains(@class, 'core-rail')]")
print(posts_section)
# Count the number of posts in the section
#posts_count = len(posts_section.find_elements(By.XPATH, ".//li[contains(@class, 'feed-shared-update-v2')]"))
#print(f"Number of posts in the specified month: {posts_count}")

# Close the WebDriver
driver.quit()
