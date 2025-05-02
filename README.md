

# PyL360 ![Static Badge](https://img.shields.io/badge/0.1.5-green?logo=%5C&label=PyPI&link=https%3A%2F%2Fpypi.org%2Fproject%2FPyL360%2F)

This is a Python library to interact with Life360, primarily to read data.


## Usage
First install the package by running `pip install PyL360`. Example to print out a list of all users and their current location in all your circles
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
			if (p.location is not None):
				print("{} is at ({},{})".format(p.firstName, p.location.latitude, p.location.longitude))
			else:
				print("{} cannot be located".format(p.firstName))

```

Example to print out a list of all the places in all your circles along with their locations
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
		for place in client.GetPlaces(circle.id).places:
			if (p.location is not None):
					print("{} is at ({},{})".format(p.firstName, p.location.latitude, p.location.longitude))
				else:
					print("{} cannot be located".format(p.firstName))
```

