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
    _initializeNewGalleryDirectories(galleryDocument)
    _populateGallery(galleryDocument, request)
    saveNewGallery(name, galleryDocument['directory'])

    info = {
        'title' : 'Adam and Anna',
        'galleries' : getGalleries(),
        'success' : 'New Gallery sucessfully created'
    }

    return template('new.html', info) 
    

def _initializeNewGalleryDocument(name):
    directory = _getNewGalleryDirectory(name)

    path = _getNewGalleryPath(directory)
    miniatures_path = _getNewMiniaturesPath(directory)

    return {
        'directory' : directory,
        'gallery_path' : path,
        'miniatures_path' : miniatures_path,
        'names': {
            'en' : name,
            'pl' : name
        }
    }   

def _getNewGalleryDirectory(name):
    return name.replace(" ","")

def _getNewGalleryPath(directory):
    return "galleries/"+directory

def _getNewMiniaturesPath(directory):
    return "miniatures/"+directory

def _initializeNewGalleryDirectories(galleryDocument):
    _initializeNewGalleryPath(galleryDocument)
    _initializeNewMiniaturesPath(galleryDocument)

def _initializeNewGalleryPath(galleryDocument):
    if not exists(galleryDocument['gallery_path']):
        makedirs(galleryDocument['gallery_path'])

def _initializeNewMiniaturesPath(galleryDocument):
    if not exists(galleryDocument['miniatures_path']):
        makedirs(galleryDocument['miniatures_path'])

def _populateGallery(galleryDocument, request):
    _copyMiniatureImages(galleryDocument, request)
    _moveImagesToGallery(galleryDocument, request)

def _copyMiniatureImages(galleryDocument, request):
    index = 1
    for miniature in request.forms.getlist('miniatures[]'):
        copyfile("tmp/"+miniature, galleryDocument['miniatures_path']+"/miniature"+str(index)+".jpg")
        index += 1

def _moveImagesToGallery(galleryDocument, request):
    pictureNames = request.forms.getlist('pics[]')
    for picture in pictureNames:
        rename("tmp/"+picture, "galleries/"+directory+"/"+picture)

@app.post('/upload')
def uploadNewImage(): 
    path = getcwd() + "/tmp/"
    return plupload.save(request.forms, request.files, path)