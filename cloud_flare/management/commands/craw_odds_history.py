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
            ips = cf.ips.get()
        except CloudFlare.exceptions.CloudFlareAPIError as e:
            exit('/ips - %d %s' % (e, e))
        except Exception as e:
            exit('/ips - %s - api call connection failed' % (e))

        print('ipv4_cidrs count = ', len(ips['ipv4_cidrs']))
        for cidr in sorted(set(ips['ipv4_cidrs'])):
            print('\t', cidr)
        print('ipv6_cidrs count = ', len(ips['ipv6_cidrs']))
        for cidr in sorted(set(ips['ipv6_cidrs'])):
            print('\t', cidr)
        exit(0)