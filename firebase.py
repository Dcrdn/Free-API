import pyrebase
import base64
import getConfig from variables

firebase=pyrebase.initialize_app(getConfig())

storage=firebase.storage()
#storage.child("images/new.jpg").put("img/perro.jpg")
#print storage.child("images/new.jpg").get_url(None)

def save(img_data, id):
    with open("image.png", "wb") as file:
        file.write(base64.b64decode(img_data))
    return saveFile("image.png", id)

def saveFile(picture, id):
    name="images/profile"+str(id)+".png"
    storage.child(name).put(picture)
    uri=storage.child(name).get_url(None)
    return uri