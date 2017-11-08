from bottle import Bottle, route, static_file

app = Bottle()

#STATIC ROUTES
@app.route('/style/<style>')
def serve_styles(style):
    return static_file(style, root='static/')

@app.route('/script/<script>')
def serve_styles(script):
    return static_file(script, root='static/')

@app.route('/picture/<picture>')
def serve_pictures(picture):
    return static_file(picture, root='static/')

@app.route('/images/<picture>')
def serve_pictures(picture):
    return static_file(picture, root='static/')

@app.route('/galleries/<gallery>/<picture>')
def serve_gallery_picture(gallery, picture):
    print(gallery)
    return static_file(picture, root='galleries/'+gallery + '/')

@app.route('/miniature/<gallery>/<name>')
def serve_pictures(gallery, name):
    return static_file(name, root='miniatures/'+gallery+'/')
