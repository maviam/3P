from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required

class Hoteis(Resource):
    def get(self):
        return { "hoteis": [hotel.json() for hotel in HotelModel.query.all()] }

class Hotel(Resource):
    
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("nome", type=str, required=True, help="nome obrigatorio")
    argumentos.add_argument("estrelas", type=float, required=True, help="estrelas obrigatorio")
    argumentos.add_argument("diaria", type=float, required=True, help="diaria obrigatorio")
    argumentos.add_argument("cidade", type=str, required=True, help="cidade obrigatorio")
    
    def get(self, id_hotel):
        hotel = HotelModel.find_hotel()
        if hotel:
            return hotel.json(), 200
        return { "message": "hotel not found" }, 404

    @jwt_required()
    def post(self, id_hotel):
        dados = Hotel.argumentos.parse_args() # dicionario
        hotel = HotelModel.find_hotel(id_hotel)
        if hotel:
            return { "message": "hotel with this id already exists"}
        try:
            novo_hotel = HotelModel(id_hotel, **dados)
            novo_hotel.save_hotel()
            return novo_hotel.json(), 200
        except:
            return { "message": "internal error..."}, 500 # internal error

    @jwt_required()
    def put(self, id_hotel):
        dados = Hotel.argumentos.parse_args() # dicionario
        hotel = HotelModel.find_hotel(id_hotel)
        if hotel:
            try:
                hotel.update_hotel(dados["nome"], dados["estrelas"], dados["diaria"], dados["cidade"])
                hotel.save_hotel()
                return hotel.json(), 200
            except:
                return { "message": "internal error..."}, 500 # internal error
        try:
            novo_hotel = HotelModel(id_hotel, **dados)
            novo_hotel.save_hotel()
            return novo_hotel.json(), 201 # Created
        except:
            return { "message": "internal error..."}, 500 # internal error

    @jwt_required()
    def delete(self, id_hotel):
        hotel = HotelModel.find_hotel(id_hotel)
        if hotel:
            try:
                hotel.delete_hotel()
                return { "message": "hotel deleted"}, 200
            except:
                return { "message": "internal error..."}, 500 # internal error
        return  { "message": "hotel not found"}, 404