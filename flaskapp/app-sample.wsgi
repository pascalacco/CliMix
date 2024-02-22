import sys
activate_this = '/var/www/climix-test/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))
sys.path.insert(0, '/var/www/climix-test/')
sys.path.insert(0, '/var/www/climix-test/flaskapp')
from app import app as application
