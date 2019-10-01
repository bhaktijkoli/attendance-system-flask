from app import app
@app.route('/')
def get():
    return "Welcome To API"
