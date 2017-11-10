from bottle import run, template, get, mount

from databaseHandler import getGalleries, getGalleryData
import staticFilesServer
import newGalleryAppController

#CONTROLLERS
@get('/')
def viewIndexPage():
    viewData = {
        'title' : 'Adam and Anna',
        'galleries' : getGalleries()
    }
    return template('mainPage/index.html', viewData)

@get('/galleries/<galleryId>')
def viewGallery(galleryId):
    name, imagesPaths = getGalleryData(galleryId)
    viewData = {
        'title' : name,
        'directory' : galleryId,
        'imagesPaths' : imagesPaths,
        'galleries' : getGalleries()
    }
    return template('mainPage/view.html', viewData)

def main():
    mount('static/', staticFilesServer.app)
    mount('new', newGalleryAppController.app)
    run(host='0.0.0.0', port=8080, debug=True)

if __name__ == "__main__":
    main()

