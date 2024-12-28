from typing import Optional
import requests
import urllib3.util
from dto_models import DtoModels
import urllib3
from dacite import from_dict, Config
import os
import tls_client
import logging

class L360Client:
    _username: str
    _password: str
    _endpoint: str
    _initial_auth_token: str
    _logger:logging.Logger
    _token:str
    

    def __init__(
        self,
        username: str,
        password: str,
        endpoint: str = "https://api-cloudfront.life360.com",
        initial_auth_token: str = "Basic Y2F0aGFwYWNyQVBoZUtVc3RlOGV2ZXZldnVjSGFmZVRydVl1ZnJhYzpkOEM5ZVlVdkE2dUZ1YnJ1SmVnZXRyZVZ1dFJlQ1JVWQ==",
    ):
        """Constructor

        Args:
            username (str): Username for the account
            password (str): Password for the account
            endpoint (_type_, optional): Endpoint used to communicate with the service. Defaults to "https://api-cloudfront.life360.com".
            initial_auth_token (str, optional): The inital token used to authenticate.
        """
        self._username = username
        self._password = password
        self._endpoint = endpoint
        self._token = initial_auth_token
        self._logger = logging.getLogger("l360")

    def _getSession(self) -> tls_client.Session:
        return tls_client.Session(
            client_identifier="okhttp4_android_13",
            random_tls_extension_order=True
        )
        
    def _getHeaders(self):
        return {
            "User-Agent": "com.life360.android.safetymapd/KOKO/24.50.0 android/13",
            "Accept": "application/json",
            "Authorization": self._token
        }
        
    def _getUrl(self, relative_url: str):
        return self._endpoint + relative_url

    def Authenticate(self, replace_token: bool = False) -> Optional[str]:
        """Authenticates the user. If a token is cached, it will return that unless specified otherwise

        Args:
            replace_token (bool, optional): If true, will get a new token. Defaults to False.

        Returns:
            Optional[str]: Token
        """
        token_filename = "l360.token"
        
        # Check if we are not replacing the token and if so,
        # check if the token file exists and try to 
        if not replace_token and os.path.isfile(token_filename):
            try:
                saved_token = ""
                with open(token_filename, "r") as file:
                    saved_token = file.read()

                if saved_token:
                    self._token = saved_token
                    return saved_token
            except Exception as exception:
                self._logger.error(exception)


        # Get a new session with a spoofed TLS fingerprint
        session = self._getSession()
        result = session.post(
            url=self._getUrl("/v3/oauth2/token"),
            headers=self._getHeaders(),
            data={
                "username": self._username,
                "password": self._password,
                "grant_type": "password",
            },
        )
        
        # If not status 200, log error
        if result.status_code != 200:
            self._logger.critical("Failed to login")
            self._logger.critical(result.text)
            return None
        
        # Deserialize the json response
        response = from_dict(
            data_class=DtoModels.AuthenticationResponseDtoMode,
            data=result.json(),
            config=Config(strict_unions_match=False),
        )

        # Combinee the new token and set it as the Authorization
        # header and try to save it to fine
        token = response.token_type + " " + response.access_token
        self._token = token
        try:
            with open(token_filename, "w") as file:
                file.write(token)
        except Exception as exception: 
            self._logger.warning("Something went wrong when trying to save token file")
            self._logger.warning(exception)
        return token

    def GetCircles(self) -> DtoModels.GetCirclesResponse:
        session = self._getSession()
        result = session.get(
            url=self._getUrl("/v4/circles"),
            headers=self._getHeaders()
        )
        response = from_dict(
            data_class=DtoModels.GetCirclesResponse,
            data=result.json(),
            config=Config(strict_unions_match=False),
        )
        return response

    
        