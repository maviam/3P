from flask_restful import Resource, reqparse
from models.user import UserModel
from hmac import compare_digest
from flask_jwt_extended import create_access_token

class User(Resource):
    def get(self, username):
        user = UserModel.find_user()
        if user:
            return user.json(), 200
        return { "message": "User not found" }, 404
    
    def delete(self, username):
        user = UserModel.find_user(username)
        if user:
            try:
                user.delete_user()
                return { "message": "User deleted"}, 200
            except:
                return { "message": "internal error..."}, 500 # internal error
        return  { "message": "User not found"}, 404

class UserRegister(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("username", type=str, required=True, help="Username obrigatorio")
    argumentos.add_argument("password", type=str, required=True, help="Password obrigatoria")

    def post(self, username):
        dados = UserRegister.argumentos.parse_args() # dicionario
        user = UserModel.find_user(username)
        if user:
            return { "message": "User with this username already exists"}
        try:
            new_user = UserModel(**dados)
            new_user.save_user()
            return new_user.json(), 200
        except:
            return { "message": "Internal error..."}, 500 # internal error

class UserLogin(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("username", type=str, required=True, help="Username obrigatorio")
    argumentos.add_argument("password", type=str, required=True, help="Password obrigatoria")

    def post(self):
        dados = UserLogin.argumentos.parse_args()
        user = UserModel.find_user(dados["username"])

        if user and compare_digest(user.password, dados["password"]):
            token = create_access_token(identity=user.username)
            return { "access_token": token }, 200
        return { "message": "User or password invalid!" }, 401

class UserLogout(Resource):
    ...