from app import app
from routes import router

app.register_blueprint(router)

if __name__ == "__main__":
    app.run(debug=True)