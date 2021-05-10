# Covid-Vaccine-Availability-India
Check Vaccine Availability in India

For Linux/Mac users only
## Steps:
### 1. install python package
```
sudo pip3 install telegram-send
```
More info here: https://pypi.org/project/telegram-send/#examples

### 2. Create a Telegram Bot
Follow this: https://medium.com/@robertbracco1/how-to-write-a-telegram-bot-to-send-messages-with-python-bcdf45d0a580

### 3. Congigure Telegram Bot
```
telegram-send --configure
```
Add token to allow this program to send notification/messages to newly created bot

### 4. Give executable permision to the python file
```
sudo chmod +x check_vaccine_availability.py
```

### 5. Create a Cron job in linux system
Command line:
```
crontab -e
```
(select editor)
#Add below line (10 indicates cron will run every 10 minutes)
```
*/10 * * * * /usr/bin/env python3 /path/to/check_vaccine_availability.py
```

### 5. Done!

Make sure you change your pincode in the code file.
