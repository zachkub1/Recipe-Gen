from website import create_app, db
from flask_migrate import Migrate
from flask import Flask

app = create_app()
migrate = Migrate(app, db)


