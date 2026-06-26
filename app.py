from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Le serveur Flask de mon Teambuilder fonctiooooonne !"
