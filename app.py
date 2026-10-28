from flask import Flask
from flask_restful import Resource, Api
from resources.hotel import Hoteis, Hotel
from resources.user import User, UserRegister, UserLogin, UserLogout
from conexao import bd
from flask_jwt_extended import JWTManager

app = Flask(__name__)

# Configuracao da API
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hoteis.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "my_secret_key_has_to_be_always_sempre"

api = Api(app)
jwt = JWTManager(app) 

# Rotas
api.add_resource(Hoteis,"/hoteis")
api.add_resource(Hotel,"/hoteis/<string:id_hotel>")
api.add_resource(User,"/users/<string:username>")
api.add_resource(UserRegister,"/registar")
api.add_resource(UserLogin,"/login")
api.add_resource(UserLogout,"/logout")

# Iniciar a aplicacao
if __name__ ==  "__main__":
    bd.init_app(app)
    with app.app_context():
        bd.create_all()
    app.run(debug=True)
