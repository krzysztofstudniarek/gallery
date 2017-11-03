from couchdb import Server
from os import listdir
from os.path import isfile, join

couch = Server('http://0.0.0.0:5984/')

def getDocs():
    db = getDocDatabase()

    docs = db.view('_all_docs', include_docs=True);
    data = []

    for item in docs:
        data.append(item.doc)
    
    return data

def getGalleryData(directory):
    db = getDocDatabase()
    documents = db.view('_all_docs', include_docs=True);
    name = ''
    
    path = 'galleries/'+directory+'/'
    data = [f for f in listdir(path) if isfile(join(path, f))]

    for document in documents:
        if document.doc['directory'] == directory :
            name = document.doc['names']['pl']
            return name, data
    
    raise Exception('No gallery of that name') 


def saveNewGallery(name, directory):
    db = getDocDatabase()

    db.save({
        'directory' : directory,
        'type' : 'directory',
        'names':{
            'en' : name,
            'pl' : name
            }
        })

def getDocDatabase():
    try:
        db = couch['directories']
    except:
        db = couch.create('directories')

    return db

    