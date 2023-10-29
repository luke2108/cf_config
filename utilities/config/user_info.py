import requests
from requests import Response, codes
from rest_framework import exceptions

class UserInfo:
    URL = 'https://pro.ip-api.com'

    def __init__(self):
        self.headers = {}

    def get(self, url: str, params: dict = None, retry=True, **kwargs) -> Response:
        headers = self.headers | kwargs.get("headers", {})
        response = requests.get(self.URL + url, params, headers=headers, **kwargs)
        ok = self._check_status_code(response.status_code)

        if not ok and retry:
            return self.get(url, params, retry=False, **kwargs)

        return response
    
    def _check_status_code(self, status_code: int):
       
        if status_code == codes.bad_request:
            raise exceptions.ParseError()

        elif status_code == codes.unauthorized:
            raise exceptions.AuthenticationFailed()

        elif status_code == codes.forbidden:
            raise exceptions.PermissionDenied()

        elif status_code == codes.not_found:
            raise exceptions.NotFound()

        elif status_code == codes.internal_server_error:
            raise exceptions.APIException()

        return True
