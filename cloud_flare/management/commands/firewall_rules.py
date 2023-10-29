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

        zone_name = "123betvn1.com"
        filter_name = "FILTER-1"

        def get_zone_id(cf, zone_name):
            try:
                params = {'name': zone_name}
                zones = cf.zones.get(params=params)
                if len(zones) > 0:
                    return zones[0]['id']
            except Exception as e:
                print(f"Error getting zone ID: {e}")
            return None

        def get_filter(cf, zone_id, filter_name):
            try:
                filters = cf.zones.filters.get(zone_id)
                existing_filter = next((filter for filter in filters if filter['ref'] == filter_name), None)
                return existing_filter
            except Exception as e:
                print(f"Error getting filter: {e}")
            return None

        def create_filter(cf, zone_id, filter_name):
            my_filter = {
                'id': '00000000000000000000000000000123',
                'action': 'js_challenge',
                'expression': '(not ip.geoip.country in {"VN"} and not cf.client.bot)',
                'description': 'JS Challenge for non-VN and non-bot traffic',
                'ref': filter_name,
                # 'paused': False,
                'priority': 1,
            }
            try:
                filter_response = cf.zones.filters.post(zone_id, data=[my_filter])
                print(f"Filter '{filter_name}' created:\n{filter_response}")
            except Exception as e:
                print(f"Error creating filter: {e}")

        def update_filter(cf, zone_id, filter_name, paused):
            existing_filter = get_filter(cf, zone_id, filter_name)
            if existing_filter:
                existing_filter['paused'] = paused
                try:
                    filter_response = cf.zones.filters.put(zone_id, data=[existing_filter])
                    print(f"Filter '{filter_name}' updated:\n{filter_response}")
                except Exception as e:
                    print(f"Error updating filter: {e}")

        zone_id = get_zone_id(cf, zone_name)
        existing_filter_current = get_filter(cf, zone_id, filter_name)

        if existing_filter_current is not None:
            update_filter(cf, zone_id, filter_name, paused=False)
        else:
            create_filter(cf, zone_id, filter_name)