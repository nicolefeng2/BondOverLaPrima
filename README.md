# BondOverLaPrima
Script to help with WinECE Bond Over La Prima verification and pairings.
This is a script to automatically check if a given list of students are in ECE by searching on the CMU directory website, and then making pairings for WinECE Bond Over La Prima based on indicated preferences to be paired with a partner or someone random.

**Author: Nicole Feng (nvfeng)**


## STEP 1: Install package dependencies

`pip install -r requirements.txt`

^If the above doesn't work, you can do everything manually:
To use this script, you will need to install the pandas package (for dealing
with .csv files) and the selenium package (for dealing with web/chrome stuff):
```
pip install pandas
pip install selenium
```
Then you need to make sure you have the chromedriver installed in 
/usr/local/bin/chromedriver. You can download it and move it manually from the 
website.

If you have Mac, you can use homebrew:
`brew install chromedriver`

## STEP 2: Import the google form responses as a .csv
- Export the Google Form results as a .csv and then upload the download into the 
local folder where you have this script.
- In config.json, replace the value assigned to "input file" to be whatever the
name of your .csv file is.

## STEP 4: Run the script
`python3 verify_andrew.py`
OR (if that doesn't work):
`python verify_andrew.py`

## STEP 5: Retrieve pairings
In form_responses.csv (created by the script), there will be pairings based on
who chose to be randoms and who signed up with partners. Simply copy and paste 
a single row into an email recipient window to send the voucher to a pair!

**Important Note: if there are an odd number of ppl, make sure that there's 1 group of 3 in form_responses.csv. Also double check that no one appears twice!**
