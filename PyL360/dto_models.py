from typing import List, Optional
from dataclasses import dataclass
import datetime


class DtoModels:
	@dataclass
	class AuthenticationResponseDtoModel:
		access_token:str
		token_type:str
		
	@dataclass
	class CircleSummary:
		id: str
		name: str
		createdAt: str 
		_client:'Optional[str]'

		def CreatedAtDatetime(self) -> datetime:
			return datetime.fromtimestamp(int(self.createdAt))

		def GetDetails(self) -> 'DtoModels.Circle':
			return self._client.GetCircle(self.id)

	@dataclass
	class GetCirclesResponse:
		circles: 'List[DtoModels.CircleSummary]'
		
	@dataclass
	class MemberFeatures:
		device: str
		smartphone: str
		nonSmartphoneLocating: str
		geofencing: str
		shareLocation: str
		shareOffTimestamp: Optional[str]
		disconnected: str
		pendingInvite: str
		mapDisplay: str

	@dataclass
	class MemberIssues:
		disconnected: str
		type: Optional[str]
		status: Optional[str]
		title: Optional[str]
		dialog: Optional[str]
		action: Optional[str]
		troubleshooting: str

	@dataclass
	class Location:
		latitude: str
		longitude: str
		accuracy: str
		startTimestamp: int
		endTimestamp: str
		since: int
		timestamp: str
		name: Optional[str]
		placeType: Optional[str]
		source: Optional[str]
		sourceId: Optional[str]
		address1: str
		address2: str
		shortAddress: str
		inTransit: str
		tripId: Optional[str]
		driveSDKStatus: Optional[str]
		battery: str
		charge: str
		wifiState: str
		speed: float
		isDriving: str
		userActivity: Optional[str]
		algorithm: Optional[str]

	@dataclass
	class CommunicationChannels:
		channel: str
		value: str
		type: Optional[str]

	@dataclass
	class Member:
		features: 'DtoModels.MemberFeatures'
		issues: 'DtoModels.MemberIssues'
		location: 'Optional[DtoModels.Location]'
		communications: 'List[DtoModels.CommunicationChannels]'
		medical: Optional[str]
		relation: Optional[str]
		createdAt: str
		activity: Optional[str]
		id: str
		firstName: str
		lastName: str
		isAdmin: str
		avatar: Optional[str]
		pinNumber: Optional[str]
		loginEmail: str
		loginPhone: str

	@dataclass
	class CircleFeatures:
		ownerId: Optional[str]
		premium: str
		locationUpdatesLeft: int
		priceMonth: str
		priceYear: str
		skuId: Optional[str]
		skuTier: Optional[str]

	@dataclass
	class Circle:
		id: str
		name: str
		color: str
		type: str
		createdAt: str
		memberCount: str
		unreadMessages: str
		unreadNotifications: str
		features: 'DtoModels.CircleFeatures'
		members: 'List[DtoModels.Member]'
		
	@dataclass
	class Place:
		id: str
		ownerId: str
		circleId: str
		name: str
		latitude: str
		longitude: str
		radius: str
		type: Optional[str]
		typeLabel: Optional[str]

	@dataclass
	class GetPlacesResponseModel:
		places: List['DtoModels.Place']
		
	@dataclass
	class GetMembersListResponseModel:
		members: List['DtoModels.Member']
  
	@dataclass
	class PollableRequest:
		requestId: str
		isPollable: str