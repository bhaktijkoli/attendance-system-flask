from app import app
@app.route('/')
def get():
    return "Welcome to API"
