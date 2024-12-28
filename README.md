# PyL360
This is a Python library to interact with Life360, primarily to read data.


## Usage
```shell
pip install PyL360
```


Example to print out a list of all users and their current location in all your circles
```py
from PyL360 import L360Client

if __name__ == '__main__':
	client = L360Client(
		username="sammy@gmail.com",
		password="my-secure-password"
	)

	client.Authenticate()
	circles = client.GetCircles().circles

	for circle in circles:
		for p in circle.GetDetails().members:
			print("{} is at ({},{})".format(p.firstName, p.location.latitude, p.location.longitude))

```

Example to print out a list of all the places in all your circles along with their locations
```py
from PyL360 import L360Client

client = L360Client(
    username="sammy@gmail.com",
    password="my-secure-password"
)

client.Authenticate()
circles = client.GetCircles().circles

for circle in circles:
    for place in client.GetPlaces(circle.id).places:
        print('{} is loacated at ({}, {})'.format(place.name, place.latitude, place.longitude))
```

