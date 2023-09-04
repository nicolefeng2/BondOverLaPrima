import time
import pandas as pd
import os
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

# Read the configuration from the JSON file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

input_file = config["input_file"]

# Load the CSV file with emails
df = pd.read_csv(input_file)
signups = df['Email Address'].tolist() # student email
partners = df['Enter the Andrew ID of your partner, or get randomly assigned to one!'].tolist() # partner ID

# merge lists
emails = []
for email in signups:
    emails.append(email.lower())

n = len(partners)
for i in range(n):
    if partners[i] != "Give me a random partner!":
        partners[i] = partners[i].strip().lower()
        if "@andrew.cmu.edu" not in partners[i]:
            partners[i] += "@andrew.cmu.edu"
        emails.append(partners[i])

# remove duplicates
emails = set(emails)

# initialize dictionary
dict = {}
for key in emails:
    dict[key] = True

# Set the path to the directory containing the ChromeDriver executable
chromedriver_path = '/usr/local/bin/chromedriver'  # Replace with the actual path to chromedriver

# Add the Chromedriver directory to the PATH environment variable
os.environ['PATH'] = f'{os.environ["PATH"]}:{chromedriver_path}'

# Create Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Example: Setting a capability

# Initialize the WebDriver with the options
print("Initializing WebDriver...")
driver = webdriver.Chrome(options=chrome_options)

# Open the website
print("Opening CMU Directory Website...")
driver.get('https://directory.andrew.cmu.edu/')  # Replace with the actual website URL

# Loop through emails
print("Looping through emails...")
not_ece = []
for email in emails:
    # Locate the search bar and enter the email
    search_input = driver.find_element(By.ID,'basicsearch')  # Replace with the actual search bar element
    search_input.clear()
    search_input.send_keys(email)
    search_input.send_keys(Keys.RETURN)

    # Wait for the search results to load
    driver.implicitly_wait(10)

    # Check if "Electrical and Computer Engineering" is present in the page source
    if not("Computer Engineering" in driver.page_source) and not("First-Year" and "General CIT" in driver.page_source):
        dict[email] = False
        not_ece.append(email)
    
# Print non-ECE Students
print("")
print("Non-ECE Students: ")
if len(not_ece) == 0:
    print("NONE")
else:
    for email in not_ece:
        print(email)

# separate into randoms and pairs
randoms = set()
pairs = []
for p1, p2 in zip(signups, partners):
    if p2 == "Give me a random partner!":
        if dict[p1] and p1 not in partners:
            randoms.add(p1)
    elif dict[p1] and dict[p2]:
        pairs.append(sorted([p1, p2]))
    elif dict[p1]:
        randoms.add(p1)
    elif dict[p2]:
        randoms.add(p2)

# pair up randoms
randoms = list(randoms)
num_randoms = len(randoms)
if num_randoms == 1:
    pairs[0].append(randoms[0])
elif num_randoms > 1:
    if not num_randoms%2: # check that there are even number of randoms
        for i in range(1,num_randoms, 2):
            p1 = randoms[i-1]
            p2 = randoms[i]
            pairs.append(sorted([p1, p2]))
    else:
        print("")
        print("Odd # of randos, make sure there's a triple")
        pairs.append([randoms[0], randoms[1], randoms[2]])
        for i in range(4, num_randoms, 2):
            p1 = randoms[i-1]
            p2 = randoms[i]
            pairs.append(sorted([p1, p2]))

# remove duplicate pairs
for i in range(len(pairs)):
    pairs[i] = tuple(pairs[i])
unique_pairs = set(pairs)

# Export ECE Students to a .csv
print("")
print('Writing pairs to pairs.csv...')
with open('pairs.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(row for row in unique_pairs)
print('Finished writing pairs to pairs.csv')

# Close the WebDriver
driver.quit()
