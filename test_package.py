from PyL360 import L360Client
import os 

if __name__ == '__main__':
	try:
		client = L360Client(
			username=os.getenv("L360_USERNAME"),
			password=os.getenv("L360_PASSWORD"),
		)

		client.Authenticate()
		circles = client.GetCircles().circles

		for circle in circles:
			for p in circle.GetDetails().members:
				pass
		exit(0)
	except Exception as e:
		print("An error occurred: {}".format(e))
		exit(1)