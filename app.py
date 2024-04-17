"""Flask Application"""

from flask import Flask
from api_v1 import v1_blueprint

app = Flask(__name__)

app.register_blueprint(v1_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
