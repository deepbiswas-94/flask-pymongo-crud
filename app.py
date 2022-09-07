from flask import Flask
import sys
from routes import router

app = Flask(__name__)
sys.dont_write_bytecode = True
app.register_blueprint(router)


if __name__ == "__main__":
    app.run(debug=True)