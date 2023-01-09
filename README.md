# Shein Order History

This script automates the process of logging into a user's Shein account, changing the website language to English, and retrieving information about their order history. It shows the total amount of money spent on Shein and the number of items bought in the terminal.

## Requirements
- [Selenium](https://pypi.org/project/selenium/)
- [forex-python](https://pypi.org/project/forex-python/)
- [webdriver-manager](https://pypi.org/project/webdriver-manager/)


## Setup
Install the required libraries using `pip install -r requirements.txt`

## Usage
1. Run the script using `python shein.py -b <browser> -u <email> -p <password>`, where `<browser>` is either `chrome` or `firefox`, `<email>` is your Shein email, and `<password>` is your Shein password
2. The script will change the website language to English and retrieve and display information about your order history in the terminal

## Notes
- The script currently only supports Chrome and Firefox.
- The script will only retrieve information about orders with the status "Shipped". Orders with any other status will be ignored.
- The script converts all prices to USD.
- The script may take some time to retrieve and process all of the information about your order history. Please be patient.
