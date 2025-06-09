import uuid
import requests
import time
import os

url_user = "http://user:5050/"
url_file = "http://file:5051/"

token_antonio = ""
uid_antonio = ""
token_ignacio = ""
uid_ignacio = ""


class Test:


    def test_create_init_user(): # Test de la creación de un usuario

        print("Creando usuario antonio con password 1234...")
        print("Debe devolver un json con el uid y el token del usuario")

        url = url_user + "user/antonio"

        headers = {
            "Content-Type": "application/json"
        }

        params = {
            "password": "1234"
        }

        response = requests.post(url, headers=headers, params=params)

        if response.status_code == 200:
            print(response.json())
        else:
            print("Error con el código de respuesta " + str(response.status_code))


    def test_get_user_uid(): # Test de la obtención del UID de un usuario

        print("\nObteniendo UID de usuario antonio con password 1234...")
        print("Debe devolver su UID")

        global token_antonio
        global uid_antonio

        url = url_user + "get_user_uid/antonio"

        headers = {
            "Content-Type": "application/json"
        }

        params = { 
            "password": "1234"
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            print(response.json())

            uid_antonio = response.json()["uid"]
            token_antonio = str(uuid.uuid5(uuid.UUID("550e8400-e29b-41d4-a716-446655440000"), str(uid_antonio)))
        else:
            print("Error con el código de respuesta " + str(response.status_code))

    
    def test_user_error(): # Test de error en iniciar sesión de un usuario
            
            print("\nIntentando iniciar sesión con una contraseña incorrecta...")
            print("Debe devolver ERROR")

            url = url_user + "user/antonio"

            headers = {
                "Content-Type": "application/json"
            }

            params = {
                "password": "12345"
            }

            response = requests.post(url, headers=headers, params=params)

            if response.status_code == 200:
                print(response.json())
            else:
                print("Error con el código de respuesta " + str(response.status_code))


    def test_get_user_uid_error(): # Test de error en obtener el UID de un usuario

        print("\nIntentando obtener el UID de un usuario con una contraseña incorrecta...")
        print("Debe devolver ERROR")

        url = url_user + "get_user_uid/antonio"

        headers = {
            "Content-Type": "application/json"
        }

        params = {
            "password": "12345"
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            print(response.json())
        else:
            print("Error con el código de respuesta " + str(response.status_code))


    def test_create_file(): # Test de la creación de un fichero

        print("Creando el fichero fichero_001.txt con el contenido 'texto de prueba del fichero'")
        print("Debe devolver OK y el nombre del fichero")

        url = url_file + "create_file"

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token_antonio
        }

        params = {
            "uid": uid_antonio,
            "filename": "fichero_001.txt",
            "content": "texto de prueba del fichero"
        }

        response = requests.post(url, headers=headers, params=params)

        if response.status_code == 200:
            print(response.json())
        else:
            print("Error con el código de respuesta " + str(response.status_code))

    
    def test_create_second_file(): # Test de la creación de un segundo fichero

        print("\nCreando el fichero fichero_002.txt con el contenido 'Segundo fichero de prueba'")
        print("Debe devolver OK y el nombre del fichero")

        url = url_file + "create_file"

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token_antonio
        }

        params = {
            "uid": uid_antonio,
            "filename": "fichero_002.txt",
            "content": "Segundo fichero de prueba"
        }

        response = requests.post(url, headers=headers, params=params)

        if response.status_code == 200:
            print(response.json())
        else:
            print("Error con el código de respuesta  " + str(response.status_code))


    def test_crear_fichero_token_error(): # Test de error en la creación de un fichero
            
            print("\nIntentando crear un fichero con un token incorrecto...")
            print("Debe devolver ERROR")
    
            url = url_file + "create_file"
    
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + "token_incorrecto"
            }
    
            params = {
                "uid": uid_antonio,
                "filename": "fichero_003.txt",
                "content": "texto de prueba del fichero"
            }
    
            response = requests.post(url, headers=headers, params=params)
    
            if response.status_code == 200:
                print(response.json())
            else:
                print("Error con el código de respuesta  " + str(response.status_code))

        
    def test_listar_documentos(): # Test de listar los ficheros de un usuario

        print("\nBuscando la biblioteca de Antonio desde la cuenta de Antonio:")
        print("Debe devolver OK y una lista con los ficheros de Antonio")

        url = url_file + "listar_documentos"

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token_antonio
        }

        params = {
            "uid": uid_antonio
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            print(response.json())
        else:
            print("Error con el código de respuesta " + str(response.status_code))


    def test_listar_documentos_error(): # Test de error en listar los ficheros de un usuario que no tiene ficheros
            
            print("\nCreando usuario nuevo con biblioteca vacía para que no haya ficheros en la biblioteca...")
            print("Debe devolver ERROR")

            url = url_user + "user/biblio_vacia"

            headers = {
                "Content-Type": "application/json"
            }

            params = {
                "password": "prueba"
            }

            response = requests.post(url, headers=headers, params=params)

            uid = response.json()["uid"]
            token = response.json()["token"]

            url = url_file + "listar_documentos"

            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            }

            params = {
                "uid": uid
            }

            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 200:
                print(response.json())
            else:
                print("Error con el código de respuesta " + str(response.status_code))


    def test_create_second_user(): # Test de la creación de un segundo usuario

        print("\nCreando usuario ignacio con password 4321...")
        print("Debe devolver un json con el uid y el token del usuario")

        global token_ignacio
        global uid_ignacio

        url = url_user + "user/ignacio"

        headers = {
            "Content-Type": "application/json"
        }

        params = {
            "password": "4321"
        }

        response = requests.post(url, headers=headers, params=params)

        if response.status_code == 200:
            print(response.json())

            uid_ignacio = response.json()["uid"]
            token_ignacio = response.json()["token"]
        else:
            print("Error con el código de respuesta " + str(response.status_code))


    def test_download_file(): # Test de descargar el contenido de un fichero perteneciente al propio usuario
            
            print("\nDescargando el fichero fichero_001.txt desde la cuenta de Antonio:")
            print("Debe devolver OK y el contenido del fichero")
    
            url = url_file + "get_file/fichero_001.txt"
    
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token_antonio
            }
    
            params = {
                "uid": uid_antonio
            }
    
            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 200:
                print(response.json())
            else:
                print("Error con el código de respuesta " + str(response.status_code))


    def test_download_file_from_other_user(): # Test de descargar el contenido de un fichero perteneciente a otro usuario y guardarlo en la biblioteca del segundo usuario

        print("\nDescargando el fichero fichero_001.txt desde la cuenta de Ignacio:")
        print("Debe devolver OK y el contenido del fichero y guardar el fichero en su biblioteca")

        url = url_file + "get_file/fichero_001.txt/" + str(uid_antonio)

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token_ignacio
        }

        params = {
            "uid": uid_ignacio
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            print(response.json())
        else:
            print("Error con el código de respuesta " + str(response.status_code))


    def test_add_content_to_file(): # Test de añadir contenido a un fichero

        print("\nAñadiendo contenido al fichero fichero_001.txt desde la cuenta de Ignacio:")
        print("Debe devolver OK y el contenido añadido")

        url = url_file + "add_content/fichero_001.txt"

        headers = {
            "Content-Type": "application",
            "Authorization": "Bearer " + token_ignacio
        }

        params = {
            "uid": uid_ignacio,
            "content": "contenido añadido por Ignacio"
        }

        response = requests.post(url, headers=headers, params=params)

        if response.status_code == 200:
            print(response.json())
        else:
            print("Error con el código de respuesta " + str(response.status_code))

    
    def test_add_content_error(): # Test de error al añadir contenido a un fichero que no existe
                
        print("\nIntentando añadir contenido a un fichero que no existe...")
        print("Debe devolver ERROR")
        
        url = url_file + "add_content/fichero_003.txt"
        
        headers = {
            "Content-Type": "application",
            "Authorization": "Bearer " + token_ignacio
        }
        
        params = {
            "uid": uid_ignacio,
            "content": "contenido añadido por Ignacio"
        }
        
        response = requests.post(url, headers=headers, params=params)
        
        if response.status_code == 200:
            print(response.json())
        else:
            print("Error con el código de respuesta " + str(response.status_code))
            
            
    def test_delete_file(): # Test de borrar un fichero

        print("\nBorrando el fichero fichero_001.txt desde la cuenta de Antonio:")
        print("Debe devolver OK")

        url = url_file + "delete_file/fichero_001.txt"

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token_antonio
        }

        params = {
            "uid": uid_antonio
        }

        response = requests.delete(url, headers=headers, params=params)

        if response.status_code == 200:
            print(response.json())
        else:
            print(response.status_code)


    def test_delete_file_error(): # Test de error al borrar un fichero que no existe
                
        print("\nIntentando borrar un fichero que no existe...")
        print("Debe devolver ERROR")
        
        url = url_file + "delete_file/fichero_003.txt"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token_antonio
        }
        
        params = {
            "uid": uid_antonio
        }
        
        response = requests.delete(url, headers=headers, params=params)
        
        if response.status_code == 200:
            print(response.json())
        else:
            print(response.status_code)
            

if __name__ == "__main__":

    time.sleep(2) # Esperamos a que los servicios estén listos a la hora de ejecutar docker compose up

    print("\n\n >>> EMPIEZA EL TEST DE user.py <<<\n\n")

    Test.test_create_init_user()
    Test.test_get_user_uid()
    Test.test_user_error()
    Test.test_get_user_uid_error()

    print("\n\n >>> TERMINA EL TEST DE user.py <<<\n\n")

    print("\n\n >>> EMPIEZA EL TEST DE file.py <<<\n\n")

    Test.test_create_file()
    Test.test_create_second_file()
    Test.test_crear_fichero_token_error()
    Test.test_listar_documentos()
    Test.test_listar_documentos_error()
    Test.test_create_second_user()
    Test.test_download_file()
    Test.test_download_file_from_other_user()
    Test.test_add_content_to_file()
    Test.test_add_content_error()
    Test.test_delete_file()
    Test.test_delete_file_error()

    print("\n\n >>> TERMINA EL TEST DE file.py <<<\n\n")