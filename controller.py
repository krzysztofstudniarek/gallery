from bottle import run, template, get, mount

from database import getGalleries, getGalleryData
import static
import new

#CONTROLLERS
@get('/')
def viewIndexPage():
    viewData = {
        'title' : 'Adam and Anna',
        'galleries' : getGalleries()
    }
    return template('index.html', viewData)

@get('/galleries/<directory>')
def viewGallery(directory):
    
    try:
        name, data = getGalleryData(directory)

        viewData = {
            'title' : name,
            'directory' : directory,
            'imagesPaths' : data,
            'galleries' : getGalleries()
        }
        return template('view.html', viewData)

    except Exception as error:
        
        viewData = {
            'title' : 'Adam and Anna',
            'galleries' : getGalleries(),
            'error' : error
        }

        return template('index.html', viewData) 

def main():
    mount('static/', static.app)
    mount('new', new.app)
    run(host='0.0.0.0', port=8080, debug=True)

if __name__ == "__main__":
    main()

