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
            Constructor of the User class

            Params:
            - name: User name
            - password: User password
            - uid: Unique identifier for the user (optional, will be generated if not provided)
            - token: Authentication token for the user (optional, will be generated if not provided)
        """

        self.name = name
        self.password = password
        self.uid = uid if uid else uuid.uuid4()
        self.token = token if token else self.generar_token()
    
        self.crear_usuario()
        

    def generar_token(self):
        """
            Generates a unique authentication token for the user based on their UID

            return: generated unique token
        """

        secret_uid = uuid.UUID("550e8400-e29b-41d4-a716-446655440000")
        return uuid.uuid5(secret_uid, str(self.uid))
    

    def crear_usuario(self):
        """
            Creates a user file with the user's data

            return: User object if the user was created successfully, None if the user already exists
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
            Static method to log in

            Params:
            - name: User name
            - password: User password

            return: User object if the user exists and the password is correct, None if could not log in
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
    
    
    @app.route("/user/<user>", methods=["POST"])
    async def user(user):
        """
            Quart method to create a user

            Parámetros:
            - user: User name

            return: JSON with the UID and token of the user if created successfully, JSON with status ERROR if not
        """

        password = request.args.get("password")
        user_creado = User.iniciar_sesion(user, password)

        if user_creado:
            return jsonify({"uid": str(user_creado.uid), "token": str(user_creado.token)})
        else:
            return jsonify({"status": "ERROR"})
    
    
    @app.route("/get_user_uid/<user>", methods=["GET"])
    async def get_user_uid(user):
        """
            Quart method to get the UID of a user

            Parámetros:
            - user: User name

            return: JSON with the UID of the user if exists, JSON with status ERROR if not
        """

        password = request.args.get("password")
        user_creado = User.iniciar_sesion(user, password)

        if user_creado:
            return jsonify({"uid": str(user_creado.uid)})
        else:
            return jsonify({"status": "ERROR"})
    

if __name__ == "__main__":

   app.run(host="0.0.0.0", port=5050)
