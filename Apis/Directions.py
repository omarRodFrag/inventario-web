from flask_cors import CORS, cross_origin
from pymongo import MongoClient
from bson import ObjectId
import os
import sys
import Backend.Functions as callMethod
from Backend.Functions import token_required

import Backend.GlobalInfo.Helpers as HelperFunctions

import Backend.GlobalInfo.Messages as ResponseMessage

from flask import Flask, jsonify, request

import json

import Backend.GlobalInfo.keys as BaseDatos
from Backend.Functions import dbConnLocal  # Para hacer la conexión a la BD
from flask_mail import Mail, Message

app = Flask(__name__)
CORS(app)




# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'omar.rod.fraf@gmail.com'
app.config['MAIL_PASSWORD'] = 'svxf owxq meja eavy'
app.config['MAIL_DEFAULT_SENDER'] = 'omar.rod.fraf@gmail.com'
mail = Mail(app)





# Ruta para el login
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('strEmail')
        password = data.get('strPassword')

        # Llamar a la función de login
        response = callMethod.fnLogin(email,password)
        return jsonify(response), response['intResponse']
    except Exception as e:
        print(str(e))
        return jsonify({'error': 'Error en la petición'}), 400

# Ruta para verificar el código MFA
@app.route('/verify', methods=['POST'])
@token_required
def verify_code(current_user):
    try:
        data = request.get_json()
        print("Datos recibidos:", data)
        
        # Ya no necesitas extraer el email del body
        email = current_user['strEmail']
        entered_code = data.get('code')

        # Buscar el código de verificación en la base de datos
        user = dbConnLocal.clUsuarios.find_one({"strEmail": email})

        if user:
            print(user)
            stored_code = user.get('verification_code')
            
            if str(entered_code) == str(stored_code):  # Compara el código ingresado con el generado
                return jsonify({'message': 'Código verificado correctamente'}), 200
            else:
                return jsonify({'message': 'Código incorrecto'}), 400
        else:
            return jsonify({'message': 'Usuario no encontrado'}), 404

    except Exception as e:
        print(str(e))
        return jsonify({'message': 'Error al verificar el código'}), 500


# API para obtener todos los productos
@app.route('/api/productos', methods=['GET'])
def obtener_productos():
    try:
        # Llama a la función en Functions.py para obtener todos los productos
        productos = callMethod.obtener_productos()
        return jsonify(productos), 200  # Retorna los productos en formato JSON
    except Exception as e:
        HelperFunctions.PrintException()
        print(str(e))
        return jsonify({'error': 'Error interno del servidor.'}), 500


# API para obtener un producto específico
@app.route('/api/producto/<int:id>', methods=['GET'])
def obtener_producto(id):
    try:
        # Llama a la función en Functions.py para obtener el producto por ID
        producto = callMethod.obtener_producto(id)
        if producto:
            return jsonify(producto), 200
        else:
            return jsonify({'error': 'Producto no encontrado'}), 404
    except Exception as e:
        HelperFunctions.PrintException()
        print(str(e))
        return jsonify({'error': 'Error interno del servidor.'}), 500


# API para agregar un producto al carrito del usuario
@app.route('/api/carrito/agregar', methods=['POST'])
def agregar_producto_carrito():
    try:
        data = request.get_json()
        idUsuario = data.get('idUsuario')
        idProducto = data.get('idProducto')

        # Llama a la función en Functions.py para agregar el producto al carrito del usuario
        resultado = callMethod.agregar_producto_carrito(idUsuario, idProducto)

        if resultado['success']:
            return jsonify({'message': 'Producto agregado al carrito'}), 200
        else:
            return jsonify({'error': 'Error al agregar el producto al carrito'}), 400
    except Exception as e:
        HelperFunctions.PrintException()
        print(str(e))
        return jsonify({'error': 'Error interno del servidor.'}), 500


# API para obtener los productos del carrito del usuario
@app.route('/api/carrito/<int:idUsuario>', methods=['GET'])
def obtener_productos_carrito(idUsuario):
    try:
        # Llama a la función en Functions.py para obtener el carrito del usuario
        carrito = callMethod.obtener_carrito(idUsuario)
        if carrito:
            return jsonify(carrito), 200
        else:
            return jsonify({'error': 'Carrito no encontrado'}), 404
    except Exception as e:
        HelperFunctions.PrintException()
        print(str(e))
        return jsonify({'error': 'Error interno del servidor.'}), 500


# API para eliminar un producto del carrito del usuario
@app.route('/api/carrito/eliminar', methods=['POST'])
def eliminar_producto_carrito():
    try:
        data = request.get_json()
        idUsuario = data.get('idUsuario')
        idProducto = data.get('idProducto')

        # Llama a la función en Functions.py para eliminar el producto del carrito
        resultado = callMethod.eliminar_producto_carrito(idUsuario, idProducto)

        if resultado['success']:
            return jsonify({'message': 'Producto eliminado del carrito'}), 200
        else:
            return jsonify({'error': 'Error al eliminar el producto del carrito'}), 400
    except Exception as e:
        HelperFunctions.PrintException()
        print(str(e))
        return jsonify({'error': 'Error interno del servidor.'}), 500



# API para eliminar el carrito del usuario
@app.route('/api/carrito/eliminar', methods=['DELETE'])
def eliminar_carrito_usuario():
    try:
        data = request.get_json()
        idUsuario = data.get('idUsuario')

        # Llama a la función en Functions.py para eliminar el carrito del usuario
        resultado = callMethod.eliminar_carrito(idUsuario)

        if resultado['success']:
            return jsonify({'message': 'Compra realizada correctamente'}), 200
        else:
            return jsonify({'error': 'Error al eliminar el carrito'}), 400
    except Exception as e:
        HelperFunctions.PrintException()
        print(str(e))
        return jsonify({'error': 'Error interno del servidor.'}), 500





# API para obtener un producto específico
@app.route('/api/usuario/<int:id>', methods=['GET'])
def obtener_usuario(id):
    try:
        # Llama a la función en Functions.py para obtener el usuario por ID
        usuario = callMethod.obtener_usuario(id)
        if usuario:
            return jsonify(usuario), 200
        else:
            return jsonify({'error': 'Usuario no encontrado'}), 404
    except Exception as e:
        HelperFunctions.PrintException()
        print(str(e))
        return jsonify({'error': 'Error interno del servidor.'}), 500
    

# API para obtener un producto específico
@app.route('/api/usuario/todos', methods=['GET'])
def obtener_usuariosAll():
    try:
        # Llama a la función en Functions.py para obtener la lista de usuarios
        usuarios = callMethod.obtener_usuariosAll()
        if usuarios:
            return (usuarios), 200
        else:
            return jsonify({'error': 'Usuarios no encontrados'}), 404
    except Exception as e:
        HelperFunctions.PrintException()
        print(str(e))
        return jsonify({'error': 'Error interno del servidor.'}), 500

# API para eliminar un producto del carrito del usuario
@app.route('/api/usuario/actualizar', methods=['PUT'])
def actualizar_Usuario():
    try:
        data = request.get_json()
        strFirstName = data.get('strFirstName')
        strLastName = data.get('strLastName')
        strEmail = data.get('strEmail')
        strPassword = data.get('strPassword')
        strPhone = data.get('strPhone')
        strAddress = data.get('strAddress')
        strPostalCode = data.get('strPostalCode')

        # Llama a la función en Functions.py para insertar el usuario
        documento_actualizado ={
            "strFirstName": strFirstName,
            "strLastName": strLastName,
            "strEmail": strEmail,
            "strPassword": strPassword,
            "strPhone": strPhone,
            "strAddress": strAddress,
            "strPostalCode": strPostalCode,
        }

        # Llama a la función en Functions.py para eliminar el producto del carrito
        resultado = callMethod.actualizar_Usuario(documento_actualizado)

        if resultado['success']:
            return jsonify({'message': 'Usuario actualizado correctamente'}), 200
        else:
            return jsonify({'error': 'Error al actualizar la informacion del usuario'}), 400
    except Exception as e:
        HelperFunctions.PrintException()
        print(str(e))
        return jsonify({'error': 'Error interno del servidor.'}), 500

if __name__ == '__main__':
    # Obtén el puerto de la variable de entorno
    port = int(os.environ.get('PORT', 5000))
    # Ejecuta la aplicación en el puerto dinámico
    app.run(host='0.0.0.0', port=port, debug=True)



