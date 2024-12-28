
from dataclasses import dataclass
import datetime
from typing import List

class DtoModels:
    @dataclass
    class AuthenticationResponseDtoMode:
        access_token:str
        token_type:str
        
    @dataclass
    class CircleSummary:
        id: str
        name: str
        createdAt: str 

        def created_at_datetime(self) -> datetime:
            return datetime.fromtimestamp(int(self.createdAt))

    @dataclass
    class GetCirclesResponse:
        circles: 'List[DtoModels.CircleSummary]'
        