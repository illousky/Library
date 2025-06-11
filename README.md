AUTHOR:
	
	- Ignacio Gonzalez Porras
	
	
EXECUTION GUIDE:

	- To run the system, open a terminal in rootless mode in the main directory of the project
	  and execute the commands "docker compose build" and "docker compose up"
	  
	  
FILE HIERARCHY:

	- /P1
		- docker-compose.yml
		
		- /client
			- /data
			- client.py
			- Dockerfile
			- requirements.txt
		
		- /file
			- /libraries
				- Here, directories will be stored with the files saved in each user's libraries
			- file.py
			- Dockerfile
			- requirements.txt
		
		- /user
			- /users
				- Here, text files with each user's information will be stored
			- user.py
			- Dockerfile
			- requirements.txt
			

FICHEROS EXTRA:
	- nada.txt: Located at the path /P1/client/data. Created for convenience to allow uploading the /data directory to GitHub. It is an empty file
	- Memoria-P1: Located in /P1. A more detailed explanation of the work done in the project and the contents of each file.
	
			
	

