import os

from app import app

from livereload import Server


server = Server(app.wsgi_app)
server.watch(os.path.join(os.getcwd(), 'app/static/*.scss'))
server.watch(os.path.join(os.getcwd(), 'app/templates/**/*.html'))
server.serve()
