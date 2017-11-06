from bottle import Bottle, template, request, get, post
from os import makedirs, rename, getcwd
from os.path import exists
from plupload import plupload
from shutil import copyfile
from database import getDocs, saveNewGallery

app = Bottle()

@app.get('/')
def viewNewGalleryForm():
    info = {
        'title' : 'Adam and Anna',
        'docs' : getDocs()
    }
    return template('new.html', info)   

@app.post('/')
def addNewGallery():
    name = request.forms.get('name')
    directory = name.replace(" ", "")

    path = "galleries/"+directory
    miniatures_path = "miniatures/"+directory
    try:
        if not exists(path):
            makedirs(path)

        if not exists(miniatures_path):
            makedirs(miniatures_path)

        index = 1
        for miniature in request.forms.getlist('miniatures[]'):
            copyfile("tmp/"+miniature, "miniatures/"+directory+"/miniature"+str(index)+".jpg")
            index += 1

        pictureNames = request.forms.getlist('pics[]')
        for picture in pictureNames:
            rename("tmp/"+picture, "galleries/"+directory+"/"+picture)
        
        saveNewGallery(name, directory)

        info = {
            'title' : 'Adam and Anna',
            'galleries' : getGalleries(),
            'success' : 'New Gallery sucessfully created'
        }
        return template('new.html', info) 
    except Exception :
        info = {
            'title' : 'Adam and Anna',
            'galleries' : getGalleries(),
            'error' : 'Something went wrong, try one more time (' + Exception +')'
        }
        return template('new.html', info) 

@app.post('/upload')
def uploadNewImage(): 
    path = getcwd() + "/tmp/"
    return plupload.save(request.forms, request.files, path)