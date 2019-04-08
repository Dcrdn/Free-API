from app import db

class Usuarios(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String())
    apellido= db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())
    edad = db.Column(db.String())
    ciudad = db.Column(db.String())
    genero = db.Column(db.String())
    estado = db.Column(db.String())
    interes = db.Column(db.String())
    fotoPerfil = db.Column(db.String())

    def __init__(self, nombre, apellido, email, password, edad, ciudad, genero, estado, interes, fotoPerfil):
        self.nombre=nombre
        self.apellido=apellido
        self.email=email
        self.password=password
        self.edad=edad
        self.ciudad=ciudad
        self.genero=genero
        self.estado=estado
        self.interes=interes
        self.fotoPerfil=fotoPerfil

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido':self.apellido,
            'email':self.email,
            'edad':self.edad,
            'genero':self.genero,
            'estado':self.estado,
            'interes':self.interes,
            'urlPerfil': self.fotoPerfil
        }

class Matches(db.Model):
    __tablename__ = 'matches'

    id = db.Column(db.Integer, primary_key=True)
    who = db.Column(db.String())
    withWhom = db.Column(db.String())


    def __init__(self, who, withWhom):
        self.who = who
        self.withWhom = withWhom

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'who': self.who,
            'with whom': self.withWhom
        }
"""
//perfil
nombre
imagen
genero
estado
"""