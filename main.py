from app import app
from routes import router
import sys

app.register_blueprint(router)
sys.dont_write_bytecode = True

if __name__ == "__main__":
    app.run(debug=True)