import os

basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE_CONNECTION_URI = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')




