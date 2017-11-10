from bottle import Bottle, template, request, get, post
from os import makedirs, rename, getcwd
from os.path import exists
from plupload import plupload
from shutil import copyfile
from databaseHandler import getGalleries, saveNewGallery

app = Bottle()

@app.get('/')
def viewNewGalleryForm():
    info = {
        'title' : 'Adam and Anna',
        'galleries' : getGalleries()
    }
    return template('newGallery/new.html', info)   

@app.post('/')
def addNewGallery():
    name = request.forms.get('name')
    
    galleryDocument = _initializeNewGalleryDocument(name)
    galleryId = saveNewGallery(galleryDocument)

    _initializeNewGalleryDirectories(galleryId)
    _populateGallery(galleryId, request)
    

    info = {
        'title' : 'Adam and Anna',
        'galleries' : getGalleries(),
        'success' : 'New Gallery sucessfully created'
    }

    return template('mainPage/index.html', info) 
    

def _initializeNewGalleryDocument(name):
    directory = _getNewGalleryDirectory(name)
    return {
        'names': {
            'en' : name,
            'pl' : name
        }
    }   

def _getNewGalleryDirectory(name):
    return name.replace(" ","")

def _initializeNewGalleryDirectories(galleryId):
    _initializeNewGalleryPath(galleryId)
    _initializeNewMiniaturesPath(galleryId)

def _initializeNewGalleryPath(galleryId):
    path = 'galleries/'+galleryId

    if not exists(path):
        makedirs(path)

def _initializeNewMiniaturesPath(galleryId):
    path = 'miniatures/'+galleryId

    if not exists(path):
        makedirs(path)

def _populateGallery(galleryId, request):
    _copyMiniatureImages(galleryId, request)
    _moveImagesToGallery(galleryId, request)

def _copyMiniatureImages(galleryId, request):
    index = 1
    for miniature in request.forms.getlist('miniatures[]'):
        copyfile("tmp/"+miniature, 'miniatures/'+galleryId+"/miniature"+str(index)+".jpg")
        index += 1

def _moveImagesToGallery(galleryId, request):
    pictureNames = request.forms.getlist('pics[]')
    for picture in pictureNames:
        rename("tmp/"+picture, "galleries/"+galleryId+"/"+picture)

@app.post('/upload')
def uploadNewImage(): 
    path = getcwd() + "/tmp/"
    return plupload.save(request.forms, request.files, path)