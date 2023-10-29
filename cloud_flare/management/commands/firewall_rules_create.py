import json
import time
from django.conf import settings
from django.core.management.base import BaseCommand
from django.forms import ValidationError
from datetime import datetime
import logging

import CloudFlare
logger = logging.getLogger(__name__)
class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        cf = CloudFlare.CloudFlare()

        try:
            zone_name = "123betvn1.com"
        except IndexError:
            exit('usage: example_bot_management.py zone_name True/False')

        # Grab the zone identifier
        try:
            params = {'name': zone_name}
            zones = cf.zones.get(params=params)
            print("zones:", zones)
        except CloudFlare.exceptions.CloudFlareAPIError as e:
            exit('/zone %d %s - API call failed' % (e, e))
        except Exception as e:
            exit('/zone.get - %s - API call failed' % (e))

        if len(zones) == 0:
            exit('/zones.get - %s - zones not found' % (zone_name))

        if len(zones) != 1:
            exit('/zones.get - %s - API call returned %d items' % (zone_name, len(zones)))

        zone_id = zones[0]['id']

        filter_name = 'FILTER-4'
        filters = cf.zones.filters.get(zone_id)
        try:
            existing_filter = next((filter for filter in filters if filter['ref'] == filter_name), None)
        except:
            existing_filter = None    
        

        if existing_filter is not None:
            exit(f'Filter "{filter_name}" already exists. Please choose a different name for the new filter.')

        # Create a new filter
        my_filter = {
            'id': '00000000000000000000000000001111',  # You can set your own filter ID
            'action': 'js_challenge',
            'description': 'JS Challenge for non-VN and non-bot traffic',
            'expression': '(not ip.geoip.country in {"VN"} and not cf.client.bot)',
            'ref': filter_name,
            'paused': False,
            'priority': 1,
            'name': 'JS Challenge'
        }

        try:
            filter_response = cf.zones.filters.post(zone_id, data=[my_filter])
            print('Filter created:\n', json.dumps(filter_response, indent=4, sort_keys=False))
        except Exception as e:
            print('Error creating filter:', e)
            exit(1)

        # Show the newly created filter
        print('filter created:\n', json.dumps(filter_response, indent=4, sort_keys=False) + '\n')