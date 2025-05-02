import PyL360
import os 

if __name__ == '__main__':
	try:
		client = PyL360.L360Client(
			username=os.getenv("L360_USERNAME"),
			password=os.getenv("L360_PASSWORD"),
		)

		client.Authenticate()
		circles = client.GetCircles().circles

		for circle in circles:
			for p in circle.GetDetails().members:
				if (p.location is not None):
					print("{} is at ({},{})".format(p.firstName, p.location.latitude, p.location.longitude))
				else:
					print("{} cannot be located".format(p.firstName))
		exit(0)
	except Exception as e:
		print("An error occurred: {}".format(e))
		exit(1)