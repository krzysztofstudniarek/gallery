from bottle import route, run, template, static_file, request, get, post
from couchdb import Server
from os import listdir, makedirs, getcwd
from os.path import isfile, join, exists, dirname

couch = Server('http://127.0.0.1:5984/')

#CONTROLLERS
@get('/')
def index():
    info = {
        'title' : 'Adam and Anna',
        'docs' : getDocs()
    }
    return template('index.html', info)

@get('/galleries/<directory>')
def viewGallery(directory):
    db = couch['directories']
    print(directory)
    documents = db.view('_all_docs', include_docs=True);
    name = ''
    for document in documents:
        if document.doc['directory'] == directory :
            name = document.doc['names']['pl']

    path = 'galleries/'+directory+'/'
    data = [f for f in listdir(path) if isfile(join(path, f))]

    info = {
        'title' : name,
        'directory' : directory,
        'data' : data,
        'docs' : getDocs()
    }
    return template('view.html', info)

@get('/new')
def newGallery():

    info = {
        'title' : 'Adam and Anna',
        'docs' : getDocs()
    }
    return template('new.html', info)   

@post('/upload')
def index():
    from plupload import plupload
    return plupload.save(request.forms, request.files, getcwd())

def getDocs():
    
    db = couch['directories']
    docs = db.view('_all_docs', include_docs=True);
    data = []

    for item in docs:
        data.append(item.doc)
    
    return data

#STATIC ROUTES
@route('/style/<style>')
def serve_styles(style):
    return static_file(style, root='static/')

@route('/script/<script>')
def serve_styles(script):
    return static_file(script, root='static/')

@route('/picture/<picture>')
def serve_pictures(picture):
    return static_file(picture, root='static/')

@route('/images/<picture>')
def serve_pictures(picture):
    return static_file(picture, root='static/')

@route('/galleries/<gallery>/<picture>')
def serve_gallery_picture(gallery, picture):
    print(gallery)
    return static_file(picture, root='galleries/'+gallery + '/')

@route('/miniature/<gallery>/<name>')
def serve_pictures(gallery, name):
    return static_file(name, root='miniatures/'+gallery+'/')

run(host='localhost', port=8080, debug=True)