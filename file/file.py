import uuid, os
from quart import Quart, request, jsonify
from hashlib import sha1

app = Quart("libreria_SI1_files")

class File:

    name = ""
    content = ""

    def __init__(self, name, content, uid):
        """
            Constructor de la clase File

            Parámetros:
            - name: Nombre del fichero
            - content: Contenido del fichero
            - uid: Identificador único del usuario asociado al fichero
        """

        self.name = name
        self.content = content
        self.uid_asociado = uid
        
        self.new_file()
        

    def new_file(self):
        """
            Crea un nuevo fichero con el contenido indicado
            
            return: JSON con el estado de la operación
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
            Crea un directorio con el identificador del usuario asociado al fichero
            
            return: Ruta del directorio creado o existente
        """

        directorio = "libraries/" + str(self.uid_asociado)

        if not os.path.exists(directorio):
            os.makedirs(directorio)
        
        return directorio
    

    @staticmethod
    def verify_token(uid, token):
        """
            Verifica si el token de autenticación es correcto

            Parámetros:
            - uid: Identificador único del usuario
            - token: Token de autenticación

            return: True si el token es correcto, False en caso contrario
        """

        return token == str(uuid.uuid5(uuid.UUID("550e8400-e29b-41d4-a716-446655440000"), str(uid)))
    

    @staticmethod
    def listar_ficheros(uid):
        """
            Lista los ficheros de un usuario

            Parámetros:
            - uid: Identificador único del usuario

            return: Lista de ficheros del usuario si existen, None en caso contrario
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
            Obtiene el contenido de un fichero

            Parámetros:
            - uid: Identificador único del usuario asociado al fichero
            - filename: Nombre del fichero
            - uid_propio: Identificador único del usuario que solicita el fichero

            return: Contenido del fichero si se ha encontrado, None en caso contrario
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
            Elimina un fichero

            Parámetros:
            - uid: Identificador único del usuario asociado al fichero
            - filename: Nombre del fichero a eliminar

            return: JSON con el estado de la operación
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
            Añade contenido a un fichero

            Parámetros:
            - uid: Identificador único del usuario asociado al fichero
            - filename: Nombre del fichero
            - content: Contenido a añadir

            return: JSON con el estado de la operación
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
            Método de quart para crear un fichero

            return: JSON con el estado de la operación y el nombre del fichero creado
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
            Método de quart para listar los ficheros de un usuario

            return: JSON con el estado de la operación y la lista de ficheros del usuario, JSON con status ERROR si no hay ficheros
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
            Método de quart para obtener el contenido de un fichero

            Parámetros:
            - filename: Nombre del fichero

            return: JSON con el estado de la operación y el contenido del fichero, JSON con status ERROR si no se ha encontrado el fichero
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
            Método de quart para eliminar un fichero

            Parámetros:
            - filename: Nombre del fichero

            return: JSON con el estado de la operación
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
            Método de quart para obtener el fichero de otro usuario y añadirlo a la biblioteca del usuario que lo solicita

            Parámetros:
            - filename: Nombre del fichero
            - uid: Identificador único del usuario asociado al fichero

            return: JSON con el estado de la operación y el contenido del fichero, JSON con status ERROR si no se ha encontrado el fichero
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
            Método de quart para añadir contenido a un fichero

            Parámetros:
            - filename: Nombre del fichero

            return: JSON con el estado de la operación
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