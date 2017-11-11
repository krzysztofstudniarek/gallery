from couchdb import Server
from os import listdir
from os.path import isfile, join

couch = Server('http://0.0.0.0:5984/')

def getGalleries():
    db = getDocDatabase()
    docs = db.view('_all_docs', include_docs=True);
    return docs

def getGalleryData(galleryId):
    db = getDocDatabase()
    document = db.get(galleryId, include_docs=True);
    print(document)
    name_pl = document['names']['pl']
    name_en = document['names']['en']
    
    path = 'galleries/'+galleryId+'/'
    imagesPaths = [f for f in listdir(path) if isfile(join(path, f))]

    return name_pl, name_en, imagesPaths


def saveNewGallery(galleryDocument):
    db = getDocDatabase()
    print("ALA MA KOTA")
    id, rev = db.save(galleryDocument)
    print(id)

    return id

def getDocDatabase():
    try:
        db = couch['directories']
    except:
        db = couch.create('directories')

    return db

    