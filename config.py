from app import app
from flaskext.mysql import MySQL

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'b169ca9901c596'
app.config['MYSQL_DATABASE_PASSWORD'] = 'b2e46d37'
app.config['MYSQL_DATABASE_DB'] = 'heroku_35e1273324ea10d'
app.config['MYSQL_DATABASE_HOST'] = 'us-cdbr-east-06.cleardb.net'
mysql.init_app(app)