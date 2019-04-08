import os
import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Book
from models import Usuarios

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/add")
def add_book():
    name=request.args.get('name')
    author=request.args.get('author')
    published=request.args.get('published')
    try:
        book=Book(
            name=name,
            author=author,
            published=published
        )
        db.session.add(book)
        db.session.commit()
        return "Book added. book id={}".format(book.id)
    except Exception as e:
	    return(str(e))

@app.route("/getall")
def get_all():
    try:
        books=Book.query.all()
        return  jsonify([e.serialize() for e in books])
    except Exception as e:
	    return(str(e))

@app.route("/get/<id_>")
def get_by_id(id_):
    try:
        book=Book.query.filter_by(id=id_).first()
        return jsonify(book.serialize())
    except Exception as e:
	    return(str(e))


@app.route("/register")
def register():
    nombre=request.args.get('nombre')
    apellido=request.args.get('apellido')
    email=request.args.get('email')
    password=request.args.get('password')
    edad=request.args.get('edad')
    ciudad=request.args.get('ciudad')
    genero=request.args.get('genero')
    estado=request.args.get('estado')
    interes=request.args.get('interes')
    fotoPerfil=request.args.get('fotoPerfil')
    try:
        usuario=Usuarios(
            nombre=nombre,
            apellido=apellido,
            email=email,
            password=password,
            edad=edad,
            ciudad=ciudad,
            genero=genero,
            estado=estado,
            interes=interes,
            fotoPerfil=fotoPerfil
        )   
        db.session.add(usuario)
        db.session.commit()
        return "User added. user id={}".format(usuario.id)
    except Exception as e:
	    return(str(e))

@app.route("/getUsers")
def get_users():
    try:
        usuarios=Usuarios.query.all()
        return  jsonify([e.serialize() for e in usuarios])
    except Exception as e:
	    return(str(e))

@app.route("/login")
def login():
    email=request.args.get('email')
    password=request.args.get('password')
    try:
        usuario = Usuarios.query.filter_by(password=password, email=email).first()
        if(usuario==None):
            dic={"success":"False", "userId":-1}
            return json.dumps(dic)
        dic={"success":"True", "userId":usuario.id}
        return json.dumps(dic)
    except Exception as e:
	    return(str(e))

@app.route("/getProfile")
def getProfile():
    userId=request.args.get('userID')
    try:
        usuario = Usuarios.query.filter_by(id=userId).first()
        name= usuario.nombre
        gender=usuario.genero
        age=usuario.edad
        userState=usuario.estado
        image=usuario.fotoPerfil
        lastName=usuario.apellido
        if usuario==None:
            dic={"success":"False", "name":None,"lastName":None, "gender":None, "age":None, "userState":None, "image":None}
            return json.dumps(dic)
        dic={"success":"True", "name":name, "lastName":lastName, "gender":gender, "age":age, "userState":userState, "image":image}
        return json.dumps(dic)
    except Exception as e:
	    return(str(e))

@app.route("/explore")
def explore():
    userId=request.args.get('userID')
    numberProfiles=request.args.get('size')
    try:
        usuario = Usuarios.query.filter_by(id=userId).first()
        intereses=usuario.interes
        victimas=Usuarios.query.filter_by(genero="male").limit(numberProfiles).all()
        dic={}
        for num in range(0,len(victimas)):
            idVictima=victimas[num].id
            fotoPerfil=victimas[num].fotoPerfil
            name=victimas[num].nombre
            data={"id":idVictima, "name":name,"imagen":fotoPerfil}
            dic[num+1]=data
        return json.dumps(dic)
    except Exception as e:
	    return(str(e))

if __name__ == '__main__':
    app.run()