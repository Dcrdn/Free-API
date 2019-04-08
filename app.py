import os
import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Usuarios
from models import Matches

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/register", methods = ['POST'])
def register():
    nombre=request.form.get('nombre')
    apellido=request.form.get('apellido')
    email=request.form.get('email')
    password=request.form.get('password')
    edad=request.form.get('edad')
    ciudad=request.form.get('ciudad')
    genero=request.form.get('genero')
    estado=request.form.get('estado')
    interes=request.form.get('interes')
    fotoPerfil=request.form.get('fotoPerfil')
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

@app.route("/getUsers", methods = ['POST', 'GET'])
def get_users():
    try:
        usuarios=Usuarios.query.all()
        return  jsonify([e.serialize() for e in usuarios])
    except Exception as e:
	    return(str(e))

@app.route("/login", methods = ['POST'])
def login():
    email=request.form.get('email')
    password=request.form.get('password')
    try:
        usuario = Usuarios.query.filter_by(password=password, email=email).first()
        if(usuario==None):
            dic={"success":"False", "userId":-1}
            return json.dumps(dic)
        dic={"success":"True", "userId":usuario.id}
        return json.dumps(dic)
    except Exception as e:
	    return(str(e))

@app.route("/getProfile", methods = ['POST'])
def getProfile():
    userId=request.form.get('userID')
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

@app.route("/explore", methods = ['POST'])
def explore():
    userId=request.form.get('userID')
    numberProfiles=request.form.get('size')
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

@app.route("/addMatch", methods = ['POST'])
def addMatch():
    userId=request.form.get('userId')
    matchWith=request.form.get('matchcWith')
    try:
        match=Matches(
            who=userId,
            withWhom=matchWith
        )
        db.session.add(match)
        db.session.commit()
        return "Match added. match id={}".format(match.id)
    except Exception as e:
	    return(str(e))

@app.route("/getMatches", methods = ['POST'])
def getMatches():
    userId=request.form.get('userId')
    try:
        #matches=Matches.query.all()
        matches = Matches.query.filter_by(who=userId).all()
        dic={}
        for num in range(0,len(matches)):
            data={"matchWith": matches[num].id}
            dic[num+1]=data
        return  json.dumps(dic)
    except Exception as e:
	    return(str(e))

if __name__ == '__main__':
    app.run()