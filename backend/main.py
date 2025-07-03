# main.py
import os
from flask import Flask
from flask_cors import CORS
from app.routes import routes

app = Flask(__name__)
CORS(app)
app.register_blueprint(routes)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # ✅ Use Render-provided port
    app.run(host="0.0.0.0", port=port, debug=True)  # ✅ Must bind to 0.0.0.0
