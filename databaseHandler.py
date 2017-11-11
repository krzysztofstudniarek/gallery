from couchdb import Server

couch = Server('http://0.0.0.0:5984/')

def getGalleries():
    db = getDocDatabase()
    docs = db.view('_all_docs', include_docs=True);
    return docs

def getGalleryData(galleryId):
    db = getDocDatabase()
    document = db.get(galleryId, include_docs=True);
    return document


def saveNewGallery(galleryDocument):
    db = getDocDatabase()
    id, rev = db.save(galleryDocument)
    print(id)

    return id

def getDocDatabase():
    try:
        db = couch['directories']
    except:
        db = couch.create('directories')

    return db

    