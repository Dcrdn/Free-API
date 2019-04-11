import os
import json
import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from firebase import save

app = Flask(__name__)
CORS(app)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Usuarios
from models import Matches
from models import Mensajes

@app.route("/")
def hello():
    print "hello world"
    return "Hello World!"

@app.route("/register", methods = ['POST'])
def register():
    dic = json.loads(request.get_data())

    nombre=dic['nombre']
    apellido=dic['apellido']
    email=dic['email']
    password=dic['password']
    edad=dic['edad']
    ciudad=dic['ciudad']
    genero=dic['genero']
    estado=dic['estado']
    interes=dic['interes']
    fotoPerfil=dic['fotoPerfil']
    fecha=str(datetime.datetime.now())
    uri=save(fotoPerfil, fecha)
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
            fotoPerfil=uri
        )   
        db.session.add(usuario)
        db.session.commit()
        dic={"userId":str(usuario.id)}
        return json.dumps(dic)
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
    dic = json.loads(request.get_data())
    email=dic['email']
    password=dic['password']
    try:
        usuario = Usuarios.query.filter_by(password=password, email=email).first()
        if(usuario==None):
            dic={"success":"False", "userId":-1}
            return json.dumps(dic)
        dic={"success":"True", "userId":str(usuario.id)}
        return json.dumps(dic)
    except Exception as e:
	    return(str(e))

@app.route("/getProfile", methods = ['POST'])
def getProfile():
    dic = json.loads(request.get_data())
    userId=dic['userID']
    try:
        
        usuario = Usuarios.query.filter_by(id=int(userId)).first()
        print "---------"
        print type(int(userId))
        print userId
        print usuario
        print "----"
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
    dic = json.loads(request.get_data())
    userId=dic['userId']
    numberProfiles=dic['size']
    try:
        usuario = Usuarios.query.filter_by(id=userId).first()
        intereses=usuario.interes
        intereses=intereses[0:-1]
        victimas=Usuarios.query.filter_by(genero=intereses).limit(numberProfiles).all()
        dic={}
        lista=[]
        for num in range(0,len(victimas)):
            idVictima=victimas[num].id
            
            matches = Matches.query.filter_by(who=str(userId), withWhom=str(idVictima)).first()
            if matches!=None:
                continue
            
            fotoPerfil=victimas[num].fotoPerfil
            name=victimas[num].nombre
            data={"id":idVictima, "name":name,"uri":fotoPerfil}
            #dic[num+1]=data
            lista.append(data)
        dic["usuarios"]=lista
        return json.dumps(dic)
    except Exception as e:
	    return(str(e))

@app.route("/addMatch", methods = ['POST'])
def addMatch():
    dic = json.loads(request.get_data())
    userId=dic['userId']
    matchWith=dic['matchWith']
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
    dic = json.loads(request.get_data())
    userId=dic['userId']
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

@app.route("/getConversations", methods = ['POST'])
def getConversations():
    dic = json.loads(request.get_data())
    userId=dic['userId']
    try:
        dic={}
        pos=1
        matches = Matches.query.filter_by(who=str(userId)).all()
        likes=[]
        lista=[]
        for i in range(0,len(matches)):
            if matches[i].withWhom in likes:
                continue
            likes.append(matches[i].withWhom)
        
        for element in likes:
            helperMatches = Matches.query.filter_by(who=str(element)).all()
            listaHelper=[]
            for num in range(0,len(helperMatches)):
                if str(helperMatches[num].withWhom) in listaHelper:
                    continue
                listaHelper.append(str(helperMatches[num].withWhom))
            
            if str(userId) not in listaHelper:
                continue
            if element==None:
                continue

            usuario=Usuarios.query.filter_by(id=int(element)).first()
            name= usuario.nombre
            image=usuario.fotoPerfil
            lastName=usuario.apellido
            mensajes = Mensajes.query.filter_by(who=str(userId), toWhom=str(element)).all()
            mensajes2 = Mensajes.query.filter_by(who=str(element), toWhom=str(userId)).all()

            if(len(mensajes)!=0 and len(mensajes2)!=0):
                m1=mensajes[-1]
                m2=mensajes2[-1]
                finalMessage=""
                if m1.id>m2.id:
                    finalMessage=m1.message
                    lastMessage="false"
                    lastId=str(userId)
                else:
                    finalMessage=m2.message
                    lastMessage="true"
                    lastId=str(element)
            elif(len(mensajes)!=0):
                m1=mensajes[-1]
                finalMessage=m1.message
                lastMessage="false"
                lastId=str(userId)
            elif (len(mensajes2)!=0):
                m2=mensajes2[-1]
                finalMessage=m2.message
                lastMessage="true"
                lastId=str(element)
            else:
                finalMessage=""
                lastMessage="false"
            temp={}
            temp["id"]=str(element)
            temp["name"]=name
            temp["lastName"]=lastName   
            temp["lastMessage"]=finalMessage
            temp["active"]=lastMessage
            temp["image"]=image
            lista.append(temp)
        dic["users"]=lista
        return  json.dumps(dic)
    except Exception as e:
	    return(str(e))

@app.route("/sendMessage", methods = ['POST'])
def sendMessage():
    dic = json.loads(request.get_data())
    who=dic['who']
    toWhom=dic['toWhom']
    message=dic['message']
    try:
        mensaje=Mensajes(
            who=who,
            toWhom=toWhom,
            message=message
        )
        db.session.add(mensaje)
        db.session.commit()
        return "Mensaje added. message id={}".format(mensaje.id)
    except Exception as e:
	    return(str(e))

@app.route("/getAllMatches", methods = ['POST', 'GET'])
def getAllMatches():
    try:
        usuarios=Matches.query.all()
        return  jsonify([e.serialize() for e in usuarios])
    except Exception as e:
	    return(str(e))

@app.route("/getMensajes", methods = ['POST', 'GET'])
def getMensajes():
    try:
        usuarios=Mensajes.query.all()
        return  jsonify([e.serialize() for e in usuarios])
    except Exception as e:
	    return(str(e))

@app.route("/getMessages", methods = ['POST'])
def getMessages():
    dic = json.loads(request.get_data())
    userId=dic['userId']
    otherUserID=dic['otherUserId']
    try:
        dic={}
        lista=[]
        mensajes = Mensajes.query.filter_by(who=str(userId), toWhom=str(otherUserID)).all()
        mensajes2 = Mensajes.query.filter_by(who=str(otherUserID), toWhom=str(userId)).all()

        for num in range(0,len(mensajes)):
            usuario = Usuarios.query.filter_by(id=int(mensajes[num].who)).first()
            temp={'id':mensajes[num].who, 'name':usuario.nombre, 'message':mensajes[num].message, 'order':mensajes[num].id }
            lista.append(temp)
        for num in range(0,len(mensajes2)):
            usuario = Usuarios.query.filter_by(id=int(mensajes2[num].who)).first()
            temp={'id':mensajes2[num].who, 'name':usuario.nombre, 'message':mensajes2[num].message, 'order':mensajes2[num].id}
            lista.append(temp)
        lista = sorted(lista, key=lambda k: k['order']) 
        dic["messages"]=lista
        return  jsonify(dic)
    except Exception as e:
	    return(str(e))

if __name__ == '__main__':
    app.run()