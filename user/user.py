import uuid, os
from quart import Quart, request, jsonify

app = Quart("libreria_SI1_users")

class User:

    name = ""
    password = ""
    uid = ""
    token = ""
    

    def __init__(self, name, password, uid=None, token=None):
        """
            Constructor de la clase User

            Parámetros:
            - name: Nombre del usuario
            - password: Contraseña del usuario
            - uid: Identificador único del usuario
            - token: Token de autenticación del usuario
        """

        self.name = name
        self.password = password
        self.uid = uid if uid else uuid.uuid4()
        self.token = token if token else self.generar_token()
    
        self.crear_usuario()
        

    def generar_token(self):
        """
            Genera un token de autenticación para el usuario

            return: Token de autenticación
        """

        secret_uid = uuid.UUID("550e8400-e29b-41d4-a716-446655440000")
        return uuid.uuid5(secret_uid, str(self.uid))
    

    def crear_usuario(self):
        """
            Crea un archivo de texto con los datos del usuario

            return: None si el usuario ya existe, self si se ha creado correctamente
        """

        file_path = "users/usuario_" + str(self.uid) + ".txt"

        if os.path.exists(file_path):
            return None

        try:
            with open(file_path, "x") as fichero_usuarios:
                fichero_usuarios.write(self.name + "\n")
                fichero_usuarios.write(self.password + "\n")
                fichero_usuarios.write("{'token': '" + str(self.token) + "', 'uid': '" + str(self.uid) + "'}")
        except:
            return None

        return self
        

    @staticmethod
    def iniciar_sesion(name, password):
        """
            Inicia sesión de un usuario

            Parámetros:
            - name: Nombre del usuario
            - password: Contraseña del usuario

            return: Usuario si se ha iniciado sesión correctamente, None si no
        """

        usuarios_dir = "users/"

        for archivo in os.listdir(usuarios_dir):
            file_path = os.path.join(usuarios_dir, archivo)

            try:
                with open(file_path, "r") as fichero_usuarios:
                    saved_name = fichero_usuarios.readline().strip()
                    saved_password = fichero_usuarios.readline().strip()

                    if saved_name == name and saved_password == password:
                        uid = archivo.split("_")[1].split(".")[0]
                        token = eval(fichero_usuarios.readline().strip())["token"]
                        return User(name, password, uid, token)
                    
                    if saved_name == name and saved_password != password:
                        return None
            except:
                continue

        return User(name, password)
    
    
    @app.route("/user/<user>", methods=["POST"]) # Esta función sirve para crear un usuario e iniciar sesión
    async def user(user):
        """
            Método de quart para crear un usuario e iniciar sesión

            Parámetros:
            - user: Nombre del usuario

            return: JSON con el UID y token del usuario si se ha creado correctamente, JSON con status ERROR si no
        """

        password = request.args.get("password")
        user_creado = User.iniciar_sesion(user, password)

        if user_creado:
            return jsonify({"uid": str(user_creado.uid), "token": str(user_creado.token)})
        else:
            return jsonify({"status": "ERROR"})
    
    
    @app.route("/get_user_uid/<user>", methods=["GET"]) # Esta función sirve para obtener el UID de un usuario
    async def get_user_uid(user):
        """
            Método de quart para obtener el UID de un usuario

            Parámetros:
            - user: Nombre del usuario

            return: JSON con el UID del usuario si existe, JSON con status ERROR si no
        """

        password = request.args.get("password")
        user_creado = User.iniciar_sesion(user, password)

        if user_creado:
            return jsonify({"uid": str(user_creado.uid)})
        else:
            return jsonify({"status": "ERROR"})
    

if __name__ == "__main__":

   app.run(host="0.0.0.0", port=5050)
