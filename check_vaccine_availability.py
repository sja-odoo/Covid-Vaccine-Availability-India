# -*- coding: utf-8 -*-

"""
Developed by: Sanay Jamod
Email: sjamod9@gmail.com
"""

import logging
import requests
import telegram_send

from datetime import date

_logger = logging.getLogger(__name__)

today = date.today().strftime("%d-%m-%Y")
pin_code = 380015
age_group = 18
# age_group = 45
URL = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin'
params = {'pincode': pin_code, 'date': today}
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
try:
    response = requests.get(url=URL, params=params, headers=headers)
    if response.status_code == 200:
        response = response.json()
        is_slot_available = False
        for center in response.get('centers', []):
            sessions = center.get('sessions', [])
            if any([s.get('min_age_limit', 0) == age_group for s in sessions]):
                is_slot_available = True
                name = 'Name: ' + center.get('name', '')
                address = 'Address: ' + center.get('address', '')
                vaccine = 'Vaccine: ' + sessions[0].get('vaccine', '')
                min_age_limit = 'Age Group: ' + str(sessions[0].get('min_age_limit', ''))
                telegram_send.send(messages=[name, address, vaccine, min_age_limit])
                _logger.info("Vaccine available at center: %s" % center)
        if not is_slot_available:
            _logger.info("Vaccine Slots not available for 18+ age group at this pincode: %d" % pin_code)
except Exception as ex:
    _logger.info("Error: %s" % str(ex))
