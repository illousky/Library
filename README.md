AUTOR:
	
	- Ignacio González Porras
	
	
GUIA DE EJECUCION:

	- Para ejecutar el sistema, abrir una terminal en modo rootless en el directorio principal de la práctica
	  y ejecutar los comandos "docker compose build" y "docker compose up"
	  
	  
JERARQUÍA DE FICHEROS:

	- /P1
		- docker-compose.yml
		
		- /client
			- /data
			- client.py
			- Dockerfile
			- requirements.txt
		
		- /file
			- /libraries
				- Aqui se almacenarán directorios con los ficheros guardados en las bibliotecas de cada usuario
			- file.py
			- Dockerfile
			- requirements.txt
		
		- /user
			- /users
				- Aqui se almacenarán ficheros de texto con la información de cada usuario
			- user.py
			- Dockerfile
			- requirements.txt
			

FICHEROS EXTRA:
	- nada.txt: Ubicado en el path /P1/client/data. Creado por comodidad para poder subir el directorio /data a github. Es un fichero vacío
	- Memoria-P1: Ubicado en /P1. Explicación más detallada de lo realizado en la práctica y de los contenidos de cada fichero.
	
			
	

