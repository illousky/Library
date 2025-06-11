import uuid, os
from quart import Quart, request, jsonify
from hashlib import sha1

app = Quart("libreria_SI1_files")

class File:

    name = ""
    content = ""

    def __init__(self, name, content, uid):
        """
            Constructor of the File class
            
            Params:
            - name: Name of the file
            - content: Content of the file
            - uid: Unique identifier of the user associated with the file
            
            Initializes a new file with the given name and content, and associates it with the user identified by uid.
        """

        self.name = name
        self.content = content
        self.uid_asociado = uid
        
        self.new_file()
        

    def new_file(self):
        """
            Creates a new file with the given content
            
            return: JSON with the status of the operation
        """

        file_path = self.crea_directorio() + "/" + self.name

        try:
            with open(file_path, "x") as fichero:
                fichero.write(self.content)
                return jsonify({"status": "OK"})
        except:
            return jsonify({"status": "ERROR"})
        

    def crea_directorio(self):
        """
            Creates a directory for the user if it does not exist
            
            return: Path to the directory where the file will be stored
        """

        directorio = "libraries/" + str(self.uid_asociado)

        if not os.path.exists(directorio):
            os.makedirs(directorio)
        
        return directorio
    

    @staticmethod
    def verify_token(uid, token):
        """
            Verifies if the token is correct for the given user ID

            Params:
            - uid: Unique identifier of the user
            - token: Token to verify

            return: True if the token is valid, False otherwise
        """

        return token == str(uuid.uuid5(uuid.UUID("550e8400-e29b-41d4-a716-446655440000"), str(uid)))
    

    @staticmethod
    def listar_ficheros(uid):
        """
            Lists the files of a user

            Params:
            - uid: Unique identifier of the user
            
            return: List of files if found, None if the directory does not exist or is empty
        """

        directorio = "libraries/" + str(uid)

        if not os.path.exists(directorio):
            return None

        lista_ficheros = os.listdir(directorio)
        
        if len(lista_ficheros) == 0:
            return None
        
        return lista_ficheros
    

    @staticmethod
    def get_file_content(uid, filename, uid_propio):
        """
            Obtains the content of a file

            Params:
            - uid: Unique identifier of the user associated with the file
            - filename: Name of the file to retrieve
            - uid_propio: Unique identifier of the user requesting the file

            return: Content of the file if found, None if the file does not exist or is not accessible
        """

        directorio = "libraries/" + str(uid)
        file_path = directorio + "/" + filename

        for file in os.listdir(directorio):
            if file == filename:
                with open(file_path, "r") as fichero:
                    content = fichero.read()
                        
                    if uid != uid_propio:
                        File(filename, content, uid_propio)
                        
                    return content
                
        return None
    

    @staticmethod
    def delete_file(uid, filename):
        """
            Deletes a file

            Params:
            - uid: Unique identifier of the user associated with the file
            - filename: Name of the file to delete

            return: JSON with the status of the operation
        """

        directorio = "libraries/" + str(uid)
        file_path = directorio + "/" + filename

        try:
            os.remove(file_path)
            return jsonify({"status": "OK"})
        except:
            return jsonify({"status": "ERROR"})
        

    @staticmethod
    def annadir_contenido(uid, filename, content):
        """
            Adds content to an existing file

            Params:
            - uid: Unique identifier of the user associated with the file
            - filename: Name of the file to which content will be added
            - content: Content to add to the file

            return: JSON with the status of the operation and the content added, JSON with status ERROR if the file does not exist
        """

        directorio = "libraries/" + str(uid)
        file_path = directorio + "/" + filename

        if os.path.exists(file_path):
            with open(file_path, "a") as fichero:
                fichero.write(content)
                return jsonify({"status": "OK", "content": content})
        else:
            return jsonify({"status": "ERROR"})


    @app.route("/create_file", methods= ["POST"])
    async def create_file():
        """
            Quart method to create a new file

            return: JSON with the status of the operation and the filename, JSON with status ERROR if the file could not be created
        """

        auth = request.headers.get("Authorization")
        auth_split = auth.split(" ")

        if auth_split[0] != "Bearer":
            return jsonify({"status": "ERROR"})
        else:
            uid = request.args.get("uid")
            name = request.args.get("filename")
            content = request.args.get("content")

            if File.verify_token(uid, auth_split[1]):
                file = File(name, content, uid)
                return jsonify({"status": "OK", "filename": file.name})
            else:
                return jsonify({"status": "ERROR"})
            
            
    @app.route("/listar_documentos", methods= ["GET"])
    async def listar_documentos():
        """
            Quart method to list the files of a user

            return: JSON with the status of the operation and the list of files, JSON with status ERROR if the user does not have any files or if the token is invalid
        """

        auth = request.headers.get("Authorization")
        auth_split = auth.split(" ")

        if auth_split[0] != "Bearer":
            return jsonify({"status": "ERROR"})
        else:
            uid = request.args.get("uid")

            if File.verify_token(uid, auth_split[1]):
                lista_ficheros = File.listar_ficheros(uid)
                
                if lista_ficheros:
                    return jsonify({"status": "OK", "ficheros": lista_ficheros})
                else:
                    return jsonify({"status": "ERROR", "Err_message": "No hay ficheros en la biblioteca"})
            else:
                return jsonify({"status": "ERROR"})

        
    @app.route("/get_file/<filename>", methods= ["GET"])
    async def get_file(filename):
        """
            Quart method to get the content of a file

            Params:
            - filename: Name of the file to retrieve
            
            return: JSON with the status of the operation and the content of the file, JSON with status ERROR if the file is not found or if the token is invalid
        """

        auth = request.headers.get("Authorization")
        auth_split = auth.split(" ")

        if auth_split[0] != "Bearer":

            return jsonify({"status": "ERROR"})
        else:
            uid = request.args.get("uid")

            if File.verify_token(uid, auth_split[1]):

                content = File.get_file_content(uid, filename, uid)

                return jsonify({"status": "OK", "content": content})
            else:
                return jsonify({"status": "ERROR"})
            

    @app.route("/delete_file/<filename>", methods= ["DELETE"])
    async def delete_file_quart(filename):
        """
            Quart method to delete a file

            Params:
            - filename: Name of the file to delete

            return: JSON with the status of the operation
        """

        auth = request.headers.get("Authorization")
        auth_split = auth.split(" ")

        if auth_split[0] != "Bearer":
            return jsonify({"status": "ERROR"})
        else:
            uid = request.args.get("uid")

            if File.verify_token(uid, auth_split[1]):
                return File.delete_file(uid, filename)
            else:
                return jsonify({"status": "ERROR"})
            
            
    @app.route("/get_file/<filename>/<uid>", methods= ["GET"])
    async def get_file_uid(filename, uid):
        """
            Quart method to get the content of a file associated with a specific user and add it to the user's library

            Params:
            - filename: Name of the file to retrieve
            - uid: Unique identifier of the user requesting the file

            return: JSON with the status of the operation and the content of the file, JSON with status ERROR if the file is not found
        """

        auth = request.headers.get("Authorization")
        auth_split = auth.split(" ")

        if auth_split[0] != "Bearer":
            return jsonify({"status": "ERROR"})
        else:
            
            uid_propio = request.args.get("uid")
            
            if File.verify_token(uid_propio, auth_split[1]):

                content = File.get_file_content(uid, filename, uid_propio)

                return jsonify({"status": "OK", "content": content})
            else:
                return jsonify({"status": "ERROR"})
            
    
    @app.route("/add_content/<filename>", methods= ["POST"])
    async def add_content(filename):
        """
            Quart method to add content to an existing file

            Params:
            - filename: Name of the file to which content will be added

            return: JSON with the status of the operation and the content added, JSON with status ERROR if the file does not exist or if the token is invalid
        """

        auth = request.headers.get("Authorization")
        auth_split = auth.split(" ")

        if auth_split[0] != "Bearer":
            return jsonify({"status": "ERROR"})
        else:
            uid = request.args.get("uid")
            
            if File.verify_token(uid, auth_split[1]):
                
                content = request.args.get("content")
                
                return File.annadir_contenido(uid, filename, content)
            else:
                return jsonify({"status": "ERROR"})                


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5051)    