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
district_id = 178
# search_by = 'pincode'
search_by = 'district'

# URL_PINCODE = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin'
URL_DISTRICT = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict'
# params_pincode = {'pincode': pin_code, 'date': today}
params_district = {'district_id': district_id, 'date': today}
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
try:
    response = requests.get(url=URL_DISTRICT, params=params_district, headers=headers)
    if response.status_code == 200:
        response = response.json()
        is_slot_available = False
        for center in response.get('centers', []):
            sessions = center.get('sessions', [])
            if any([s.get('min_age_limit', 0) == age_group and s.get('available_capacity', 0) > 0  for s in sessions]):
                is_slot_available = True
                name = 'Center Name: ' + center.get('name', '')
                address = 'Address: ' + center.get('address', '')
                vaccine = 'Vaccine: ' + sessions[0].get('vaccine', '')
                min_age_limit = 'Age Group: ' + str(sessions[0].get('min_age_limit', ''))
                slots_available = 'Available Slots: ' + str(sessions[0].get('available_capacity', 0))
                slots = sessions[0].get('slots', [])
                slot_timeframe = 'Slots: ' + ', '.join(slots)
                message = name + '\n' + address + '\n' + vaccine + '\n' + min_age_limit + '\n' + slots_available + '\n' + slot_timeframe
                telegram_send.send(messages=[message])
                _logger.info("Vaccine available at center: %s" % center)
                print("Vaccine available at center: %s" % center)

        if not is_slot_available:
            if search_by == 'pincode':
                _logger.info("Vaccine Slots not available for %d+ age group at this pincode: %d" % (age_group, pin_code))
                print("Vaccine Slots not available for %d+ age group at this pincode: %d" % (age_group, pin_code))
            else:
                _logger.info("Vaccine Slots not available for %d+ age group at this district: %d" % (age_group, district_id))
                print("Vaccine Slots not available for %d+ age group at this district: %d" % (age_group, district_id))
    else:
        _logger.info("Error in response: %s" % response.status_code)
        print("Error in response: %s" % response.status_code)
except Exception as ex:
    _logger.info("Error: %s" % str(ex))
    print("Error: %s" % str(ex))
