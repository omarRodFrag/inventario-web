from flask import Flask, jsonify, request, Response
from bson import ObjectId
from functools import wraps
import Backend.GlobalInfo.Helpers as HelperFunctions

import Backend.GlobalInfo.Messages as ResponseMessage

import bcrypt
import re
from flask_mail import Message
import json
import sys
import copy
import random
from flask_mail import Mail
import jwt
import Backend.GlobalInfo.keys as BaseDatos
from pymongo import MongoClient

import datetime
from Backend.GlobalInfo.keys import JWT_SECRET_KEY


# Connection to database
if BaseDatos.dbconn == None:
    mongoConnect = MongoClient(BaseDatos.strConnection)
    BaseDatos.dbconn = mongoConnect[BaseDatos.strDBConnection]
    dbConnLocal = BaseDatos.dbconn

mail = Mail()
from pymongo import MongoClient
import Backend.GlobalInfo.keys as BaseDatos

# Conexión a MongoDB
try:
    mongoConnect = MongoClient(BaseDatos.strConnection)
    dbConnLocal = mongoConnect[BaseDatos.strDBConnection]
    print("Conexión exitosa a MongoDB Atlas")
    
    # Prueba una simple consulta
    test_collection = dbConnLocal.clProductos.find_one()
    if test_collection:
        print("Conexión verificada, datos obtenidos.")
    else:
        print("Conexión exitosa, pero no se encontraron datos.")
    
except Exception as e:
    print("Error de conexión a MongoDB Atlas:", e)

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        # Verificar si el token está en los encabezados
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]  # Obtener el token de los encabezados
        
        if not token:
            return jsonify({'message': 'Token es requerido'}), 403
        
        try:
            # Verificar y decodificar el token
            decoded_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
            current_user = dbConnLocal.clUsuarios.find_one({"idUsuario": decoded_token['idUsuario']})
            if not current_user:
                return jsonify({'message': 'Usuario no encontrado'}), 404
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token ha expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token inválido'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated_function




def insert_usuario_log(data):
    try:
        # Verifica si el nombre contiene solamente letras
        if not re.fullmatch(r'[A-Za-zÁÉÍÓÚáéíóúñÑ]+(?: [A-Za-zÁÉÍÓÚáéíóúñÑ]+)*', data["strFirstName"]):
            print("nombre ")
            return {'error': 'El nombre solo debe contener letras y espacios.'}
        
        # Verifica si la contraseña cumple con el patrón
        patrón = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z\d]{8,}$'
        if not re.fullmatch(patrón, data["strPassword"]):
            print("contraseña ")
            return {'error': 'La contraseña no tiene el formato solicitado'}
        
        # Verifica si el correo ya está en uso
        existing_user = dbConnLocal.clUsuarios.find_one({"strEmail": data["strEmail"]})
        if existing_user:
            return {'error': 'El correo electrónico ya está en uso.'}  # Retorna un error si el correo ya existe

        # **Hashear la contraseña**
        hashed_password = bcrypt.hashpw(data["strPassword"].encode('utf-8'), bcrypt.gensalt())
        data["strPassword"] = hashed_password.decode('utf-8')  # Guardamos la contraseña como string

        # Obtener el mayor idUsuario en la colección de usuarios
        max_id_usuario = list(dbConnLocal.clUsuarios.aggregate([
            {"$group": {"_id": None, "max_idUsuario": {"$max": "$idUsuario"}}}
        ]))

        nuevo_id_usuario = 1
        if max_id_usuario:
            nuevo_id_usuario = max_id_usuario[0]["max_idUsuario"] + 1

        # Insertar el nuevo usuario con el nuevo idUsuario
        data["idUsuario"] = nuevo_id_usuario
        dbConnLocal.clUsuarios.insert_one(data)

        return {'message': 'Usuario registrado exitosamente', 'idUsuario': nuevo_id_usuario}

    except Exception as e:
        HelperFunctions.PrintException()
        return {'error': 'Error al insertar usuario.'}



# Función para obtener todos los productos
def obtener_productos():
    try:
        # Obtener todos los productos de la colección "productos"
        productos = list(dbConnLocal.clProductos.find({}))
        
        # Convertir los resultados a una lista de diccionarios
        productos = [{
            "_id": producto["_id"],
            "name": producto["name"],
            "image": producto["image"],
            "price": producto["price"],
            "rating": producto["rating"],
            "reviews": producto["reviews"],
            "best_seller": producto["best_seller"],
            "sizes": producto["sizes"],
            "shipping_from": producto["shipping_from"],
            "seller": producto["seller"],
            "return_policy": producto["return_policy"],
            "description": producto["description"],
            "category": producto["category"]
        } for producto in productos]

        return productos
    except Exception as e:
        HelperFunctions.PrintException()
        return {'error': 'Error al obtener los productos.'}




# Función para obtener un producto específico por ID
def obtener_producto(id):
    try:
        # Buscar el producto por _id
        producto = dbConnLocal.clProductos.find_one({"_id": id})

        if producto:
            return {
                "_id": producto["_id"],
                "name": producto["name"],
                "image": producto["image"],
                "price": producto["price"],
                "rating": producto["rating"],
                "reviews": producto["reviews"],
                "best_seller": producto["best_seller"],
                "sizes": producto["sizes"],
                "shipping_from": producto["shipping_from"],
                "seller": producto["seller"],
                "return_policy": producto["return_policy"],
                "description": producto["description"],
                "category": producto["category"]
            }
        else:
            return None
    except Exception as e:
        HelperFunctions.PrintException()
        return None



# Función para agregar un producto al carrito del usuario
def agregar_producto_carrito(idUsuario, idProducto):
    try:
        # Verifica si el carrito ya existe para el usuario
        carrito = dbConnLocal.clCarritos.find_one({"idUsuario": idUsuario})

        if not carrito:
            # Si el carrito no existe, crea uno nuevo
            dbConnLocal.clCarritos.insert_one({"idUsuario": idUsuario, "productos": [idProducto]})
        else:
            # Si el carrito existe, agrega el producto al carrito
            dbConnLocal.clCarritos.update_one(
                {"idUsuario": idUsuario},
                {"$push": {"productos": idProducto}}
            )

        return {'success': True}
    except Exception as e:
        HelperFunctions.PrintException()
        return {'success': False}



# Función para obtener los productos del carrito de un usuario
def obtener_carrito(idUsuario):
    try:
        # Buscar el carrito del usuario por idUsuario
        carrito = dbConnLocal.clCarritos.find_one({"idUsuario": idUsuario})
        if carrito:
            return {
                "idUsuario": carrito["idUsuario"],
                "productos": carrito["productos"]
            }
        else:
            return None
    except Exception as e:
        HelperFunctions.PrintException()
        return None


# Función para eliminar un producto del carrito del usuario
def eliminar_producto_carrito(idUsuario, idProducto):
    try:
        # Actualiza el carrito del usuario eliminando el producto
        resultado = dbConnLocal.clCarritos.update_one(
            {"idUsuario": idUsuario},
            {"$pull": {"productos": idProducto}}
        )
        
        # Verifica si se realizó algún cambio
        if resultado.modified_count > 0:
            return {'success': True}
        else:
            return {'success': False}
    except Exception as e:
        HelperFunctions.PrintException()
        return {'success': False}



# Función para eliminar el carrito de un usuario
def eliminar_carrito(idUsuario):
    try:
        # Elimina el carrito del usuario
        resultado = dbConnLocal.clCarritos.delete_one({"idUsuario": idUsuario})

        # Verifica si se eliminó algún documento
        if resultado.deleted_count > 0:
            return {'success': True}
        else:
            return {'success': False}
    except Exception as e:
        HelperFunctions.PrintException()
        return {'success': False}
    



# Función para enviar el correo de verificación
def send_verification_email(email, code):
    try:
        msg = Message('Código de Verificación', recipients=[email])
        msg.body = f'Tu código de verificación es: {code}'
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error al enviar correo: {e}")
        return False

def fnLogin(email, password):
    try:
        # Buscar al usuario en la base de datos (sin comparar la contraseña directamente)
        jsnInfoUser = dbConnLocal.clUsuarios.find_one({"strEmail": email})
        
        if jsnInfoUser is not None:
            # Verificar la contraseña con bcrypt
            hashed_password = jsnInfoUser.get('strPassword', '')

            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')): 
                # Generar el JWT
                expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expira en 1 hora
                payload = {
                    'idUsuario': jsnInfoUser['idUsuario'],
                    'exp': expiration_time  # Fecha de expiración del token
                }
                token = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')  # Firmamos el token con la clave secreta
                
                # Generar un código de verificación aleatorio
                verification_code = random.randint(100000, 999999)

                # Almacenar el código de verificación en la base de datos
                dbConnLocal.clUsuarios.update_one(
                    {"strEmail": email},
                    {"$set": {"verification_code": verification_code}}
                )

                # Enviar el código de verificación por correo electrónico
                email_sent = send_verification_email(jsnInfoUser['strEmail'], verification_code)
                if email_sent:
                    # Preparar la respuesta con el token y mensaje de correo enviado
                    jsnResponse = {
                        'strEmail': jsnInfoUser['strEmail'],
                        'strFirstName': jsnInfoUser['strFirstName'],
                        'idUsuario': jsnInfoUser['idUsuario'],
                        'token': token,  # Agregar el token a la respuesta
                        'role': jsnInfoUser['role']
                    }
                    return {'intResponse': 200, 'Result': {'usuario': jsnResponse, 'message': 'Código de verificación enviado al correo.'}}
                else:
                    return {'intResponse': 500, 'Result': {'error': 'No se pudo enviar el correo de verificación.'}}
            else:
                return {'intResponse': 203, 'Result': {'usuario': {}, 'error': 'Usuario o contraseña incorrecta'}}  # Contraseña incorrecta
        else:
            return {'intResponse': 203, 'Result': {'usuario': {}, 'error': 'Usuario no encontrado'}}  # Usuario no encontrado
    except Exception as exception:
        print('fnLogin', exception)
        return {'intResponse': 500}  # Error interno del servidor
    
    

# Función para obtener todos los productos
def obtener_usuariosAll():
    try:
        # Obtener todos los productos de la colección "productos"
        usuarios = list(dbConnLocal.clUsuarios.find({}))
        
        # Convertir los resultados a una lista de diccionarios
        usuarios = [{
            "_id": str(usuario["_id"]),
            "strFirstName": usuario["strFirstName"],
            "strLastName": usuario["strLastName"],
            "strEmail": usuario["strEmail"],
            "strPassword": usuario["strPassword"],
            "strPhone": usuario["strPhone"],
            "strAddress": usuario["strAddress"],
            "strPostalCode": usuario["strPostalCode"],
            "idUsuario": usuario["idUsuario"],
        } for usuario in usuarios]

        return usuarios
    except Exception as e:
        HelperFunctions.PrintException()
        return {'error': 'Error al obtener los usuarios.'}
    
# Función para obtener un producto específico por ID
def obtener_usuario(id):
    try:
        # Buscar el producto por _id
        usuario = dbConnLocal.clUsuarios.find_one({"idUsuario": id})

        if usuario:
            return {
                "_id": str(usuario["_id"]),
                "strFirstName": usuario["strFirstName"],
                "strLastName": usuario["strLastName"],
                "strEmail": usuario["strEmail"],
                "strPassword": usuario["strPassword"],
                "strPhone": usuario["strPhone"],
                "strAddress": usuario["strAddress"],
                "strPostalCode": usuario["strPostalCode"],
                "idUsuario": usuario["idUsuario"],
            }
        else:
            return None
    except Exception as e:
        HelperFunctions.PrintException()
        return None
    

def actualizar_Usuario(data):
    try:
        # Verifica si el usuario existe en la base de datos
        usuario = dbConnLocal.clUsuarios.find_one({"strEmail": data["strEmail"]})
        
        if not usuario:
            return {'success': False, 'error': 'Usuario no encontrado'}

        # Construir el diccionario de actualización sin valores nulos
        update_data = {k: v for k, v in data.items() if v is not None}

        # Hashear la nueva contraseña si se proporciona
        if "strPassword" in update_data:
            update_data["strPassword"] = bcrypt.hashpw(update_data["strPassword"].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Realizar la actualización en la base de datos
        resultado = dbConnLocal.clUsuarios.update_one(
            {"strEmail": data["strEmail"]},
            {"$set": update_data}
        )

        if resultado.modified_count > 0:
            return {'success': True, 'message': 'Usuario actualizado correctamente'}
        else:
            return {'success': False, 'error': 'No se realizaron cambios en el usuario'}

    except Exception as e:
        HelperFunctions.PrintException()
        return {'success': False, 'error': 'Error al actualizar el usuario'}

