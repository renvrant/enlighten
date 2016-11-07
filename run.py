import os

from livereload import Server

from app import app


server = Server(app.wsgi_app)
server.watch(os.path.join(os.getcwd(), 'app/static/*.scss'))
server.watch(os.path.join(os.getcwd(), 'app/templates/**/*.html'))
server.serve()
