from app import create_app
from flask.cli import FlaskGroup

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 