from bottle import run, template, get, mount

from database import getDocs, getGalleryData
import static
import new

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
    
    try:
        name, data = getGalleryData(directory)

        info = {
            'title' : name,
            'directory' : directory,
            'data' : data,
            'docs' : getDocs()
        }
        return template('view.html', info)

    except Exception as error:
        
        info = {
            'title' : 'Adam and Anna',
            'docs' : getDocs(),
            'error' : error
        }

        return template('index.html', info) 

def main():
    mount('static/', static.app)
    mount('new', new.app)
    run(host='0.0.0.0', port=8080, debug=True)

if __name__ == "__main__":
    main()

