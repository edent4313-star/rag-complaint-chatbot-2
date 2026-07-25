from flask import Flask
from flask_cors import CORS

from routes.dashboard import dashboard_bp
from routes.chat import chat_bp
from routes.evaluation import evaluation_bp

app = Flask(__name__)

CORS(app)

app.register_blueprint(dashboard_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(evaluation_bp)


@app.route("/")
def home():
    return {
        "project": "Complaint Intelligence Platform",
        "version": "1.0",
        "status": "Running",
    }


if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=5000)
