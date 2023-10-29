import time
from django.conf import settings
from django.core.management.base import BaseCommand
from django.forms import ValidationError
from datetime import datetime
import logging
import os
import requests

logger = logging.getLogger(__name__)
class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        token = os.getenv('CLOUDFLARE_API_TOKEN') if os.getenv('CLOUDFLARE_API_TOKEN') is not None else os.getenv('CF_API_TOKEN')
        print(token)

        url = "https://api.cloudflare.com/client/v4/user/tokens/verify"

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            print("Token Valid")
            data = response.json()
            print(data)
        else:
            print("Token Invalid")
            print(response.text)