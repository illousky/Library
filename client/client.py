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


    def test_create_init_user(): # User creation test

        print("Creating user with password 1234...")
        print("Should return a json with the uid and token of the user")

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
            print("Error with response code " + str(response.status_code))


    def test_get_user_uid(): # Obtain user UID test

        print("\nObtaining UID of user with password 1234...")
        print("Should return his UID")

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
            print("Error with response code " + str(response.status_code))

    
    def test_user_error(): # Error login test
            
            print("\nTrying to log in with a wrong password...")
            print("Should return ERROR")

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
                print("Error with response code " + str(response.status_code))


    def test_get_user_uid_error(): # Error obtaining user UID test

        print("\nTrying to obtain UID of user with wrong password...")
        print("Should return ERROR")

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
            print("Error with response code " + str(response.status_code))


    def test_create_file(): # Test of file creation

        print("\nCreating file fichero_001.txt with content 'texto de prueba del fichero'")
        print("Should return OK and the name of the file")

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
            print("Error with response code " + str(response.status_code))

    
    def test_create_second_file(): # Test of creating a second file

        print("\nCreating file fichero_002.txt with content 'Segundo fichero de prueba'")
        print("Should return OK and the name of the file")

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
            print("Error with response code " + str(response.status_code))


    def test_crear_fichero_token_error(): # Test of creating a file with an incorrect token
            
            print("\nTrying to create a file with an incorrect token...")
            print("Should return ERROR")
    
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
                print("Error with response code " + str(response.status_code))

        
    def test_listar_documentos(): # Test of listing the files of a user

        print("\nListing files of user Antonio:")
        print("Should return OK and a list of files")

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
            print("Error with response code " + str(response.status_code))


    def test_listar_documentos_error(): # Test of listing files with an empty library
            
            print("\nCreating a new user with an empty library:")
            print("Should return ERROR")

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
                print("Error with response code " + str(response.status_code))


    def test_create_second_user(): # Test of creating a second user

        print("\nCreating user Ignacio with password 4321:")
        print("Should return a json with the uid and token of the user")

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
            print("Error with response code " + str(response.status_code))


    def test_download_file(): # Test of downloading a file from the user's library
            
            print("\nDownloading file fichero_001.txt from Antonio's account:")
            print("Should return OK and the content of the file")
    
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
                print("Error with response code " + str(response.status_code))


    def test_download_file_from_other_user(): # Test of downloading a file from a user and saving it in the library of another user

        print("\nDownloading file fichero_001.txt from Ignacio's account:")
        print("Should return OK and the content of the file, and save the file in his library")

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
            print("Error with response code " + str(response.status_code))


    def test_add_content_to_file(): # Test of adding content to a file

        print("\nAdding content to file fichero_001.txt from Ignacio's account:")
        print("Should return OK and the new content added to the file")

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
            print("Error with response code " + str(response.status_code))

    
    def test_add_content_error(): # Test of adding content to a file that does not exist
                
        print("\nTrying to add content to a file that does not exist...")
        print("Should return ERROR")
        
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
            print("Error with response code " + str(response.status_code))
            
            
    def test_delete_file(): # Test of deleting a file from the user's library

        print("\nDeleting file fichero_001.txt from Antonio's account:")
        print("Should return OK")

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
            print("Error with response code " + str(response.status_code))


    def test_delete_file_error(): # Test of deleting a file that does not exist
                
        print("\nTrying to delete a file that does not exist...")
        print("Should return ERROR")
        
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
            print("Error with response code " + str(response.status_code))
            

if __name__ == "__main__":

    time.sleep(2) # Wait for the services to start
    os.system("clear") # Clear the terminal

    print("\n\n >>> STARTING TEST OF user.py <<<\n\n")

    Test.test_create_init_user()
    Test.test_get_user_uid()
    Test.test_user_error()
    Test.test_get_user_uid_error()

    print("\n\n >>> ENDING TEST OF user.py <<<\n\n")

    print("\n\n >>> STARTING TEST OF file.py <<<\n\n")

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

    print("\n\n >>> ENDING TEST OF file.py <<<\n\n")