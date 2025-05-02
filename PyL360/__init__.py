from typing import Optional
import requests
import urllib3.util
from .dto_models import DtoModels
import urllib3
from dacite import from_dict, Config
import os
import tls_client
import logging
from dacite.exceptions import WrongTypeError

class L360Client:
	_username: str
	_password: str
	_endpoint: str
	_initial_auth_token: str
	_logger: logging.Logger
	_token: str

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
			client_identifier="okhttp4_android_13", random_tls_extension_order=True
		)

	def _getHeaders(self):
		return {
			"User-Agent": "com.life360.android.safetymapd/KOKO/24.50.0 android/13",
			"Accept": "application/json",
			"Authorization": self._token,
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
		try:
			response = from_dict(
				data_class=DtoModels.AuthenticationResponseDtoModel,
				data=result.json(),
				config=Config(strict_unions_match=False, strict=False),
			)
		except WrongTypeError as e:
			self._printTypeError(e, result.json())

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
		"""Get a list of circles the user is in

		Returns:
				DtoModels.GetCirclesResponse: A list of circles
		"""
		session = self._getSession()
		result = session.get(
			url=self._getUrl("/v4/circles"), headers=self._getHeaders()
		)
		try:
			response = from_dict(
				data_class=DtoModels.GetCirclesResponse,
				data=result.json(),
				config=Config(strict_unions_match=False, strict=False),
			)
		except WrongTypeError as e:
			self._printTypeError(e, result.json())
		for x in response.circles: x._client = self
		return response

	def GetCircle(self, circleid: str) -> DtoModels.Circle:
		session = self._getSession()
		result = session.get(
			url=self._getUrl("/v3/circles/{}".format(circleid)),
			headers=self._getHeaders(),
		)
		try:
			response = from_dict(
				data_class=DtoModels.Circle,
				data=result.json(),
				config=Config(strict_unions_match=False, strict=False),
			)
		except WrongTypeError as e:
			self._printTypeError(e, result.json())
		return response

	def GetPlaces(self, circleid: str) -> DtoModels.GetPlacesResponseModel:
		session = self._getSession()
		result = session.get(
			url=self._getUrl("/v3/circles/{}/places".format(circleid)),
			headers=self._getHeaders(),
		)
		try:
			response = from_dict(
				data_class=DtoModels.GetPlacesResponseModel,
				data=result.json(),
				config=Config(strict_unions_match=False, strict=False),
			)
		except WrongTypeError as e:
			self._printTypeError(e, result.json())
		return response

	def GetPlace(self, circleid: str, placeid: str) -> DtoModels.Place:
		session = self._getSession()
		result = session.get(
			url=self._getUrl("/v3/circles/{}/places/{}".format(circleid, placeid)),
			headers=self._getHeaders(),
		)
		try:
			response = from_dict(
				data_class=DtoModels.Place,
				data=result.json(),
				config=Config(strict_unions_match=False, strict=False),
			)
		except WrongTypeError as e:
			self._printTypeError(e, result.json())
		return response

	def GetMembers(self, circleid: str) -> DtoModels.GetMembersListResponseModel:
		session = self._getSession()
		result = session.get(
			url=self._getUrl("/v3/circles/{}/members".format(circleid)),
			headers=self._getHeaders(),
		)
		try:
			response = from_dict(
				data_class=DtoModels.GetMembersListResponseModel,
				data=result.json(),
				config=Config(strict_unions_match=False, strict=False),
			)
		except WrongTypeError as e:
			self._printTypeError(e, result.json())
		return response

	def GetMember(self, circleid: str, memberid: str) -> DtoModels.Member:
		session = self._getSession()
		result = session.get(
			url=self._getUrl("/v3/circles/{}/members/{}".format(circleid, memberid)),
			headers=self._getHeaders(),
		)
		try:
			response = from_dict(
				data_class=DtoModels.Member,
				data=result.json(),
				config=Config(strict_unions_match=False, strict=False),
			)
		except WrongTypeError as e:
			self._printTypeError(e, result.json())
		return response

	def ForceMemberUpdate(self, circleid: str, memberid: str) -> DtoModels.PollableRequest:
		session = self._getSession()
		
		result = session.post(
			url=self._getUrl("/v3/circles/{}/members/{}/request".format(circleid, memberid)),
			headers=self._getHeaders(),
			data={
				"type": "location"
			},
		)
		try:
			response = from_dict(
				data_class=DtoModels.PollableRequest,
				data=result.json(),
				config=Config(strict_unions_match=False, strict=False),
			)
			return response
		except WrongTypeError as e:
			self._printTypeError(e, result.json())

	def _printTypeError(exception: WrongTypeError, payload: str):
		if (os.environ['PRINT_WRONG_TYPE_ERROR_PAYLOADS']):
			print(payload)
		raise exception
