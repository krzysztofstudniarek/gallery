from bottle import run, template, get, mount
from os import listdir
from os.path import isfile, join

import databaseHandler
import staticFilesServer
import newGalleryAppController

#CONTROLLERS
@get('/')
@get('/<lang>')
def viewIndexPage(lang='pl'):
    viewData = {
        'title' : 'Adam and Anna',
        'language' : lang,
        'galleries' : databaseHandler.getGalleries()
    }
    return template('mainPage/index.html', viewData)

@get('/galleries/<galleryId>/<lang>')
def viewGallery(galleryId, lang):
    document = databaseHandler.getGalleryData(galleryId)
    imagesNames = _getImagesNames(galleryId)
    viewData = _prepareGalleryViewData(document, galleryId, lang, imagesNames)
    return template('mainPage/view.html', viewData)

def _prepareGalleryViewData(document, galleryId, language, imagesNames):
    title = _getTitle(document, language)
    return _doPrepareGalleyViewData(title, language, galleryId, imagesNames)
    
def _getTitle(document, lang):
    if lang == 'pl' :
        return document['names']['pl']
    else :
        return document['names']['en']

def _doPrepareGalleyViewData(title, language, galleryId, imagesNames):
    return {
            'title' : title,
            'language' : language,
            'directory' : galleryId,
            'imagesPaths' : imagesNames,
            'galleries' : databaseHandler.getGalleries()
        }

def _getImagesNames(galleryId):
    path = 'galleries/'+galleryId+'/'
    return [f for f in listdir(path) if isfile(join(path, f))]

def main():
    mount('static/', staticFilesServer.app)
    mount('new', newGalleryAppController.app)
    run(host='0.0.0.0', port=8080, debug=True)

if __name__ == "__main__":
    main()

