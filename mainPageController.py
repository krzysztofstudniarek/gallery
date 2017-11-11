from bottle import run, template, get, mount

from databaseHandler import getGalleries, getGalleryData
import staticFilesServer
import newGalleryAppController

#CONTROLLERS
@get('/')
@get('/<lang>')
def viewIndexPage(lang='pl'):
    viewData = {
        'title' : 'Adam and Anna',
        'language' : lang,
        'galleries' : getGalleries()
    }
    return template('mainPage/index.html', viewData)

@get('/galleries/<galleryId>/<lang>')
def viewGallery(galleryId, lang):
    name_pl, name_en, imagesPaths = getGalleryData(galleryId)
    if lang == 'pl' :
        viewData = {
            'title' : name_pl,
            'language' : lang,
            'directory' : galleryId,
            'imagesPaths' : imagesPaths,
            'galleries' : getGalleries()
        }
    else :
        viewData = {
            'title' : name_en,
            'language' : lang,
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

