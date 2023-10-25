from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message

from models import db, Message

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)


@app.route("/messages", methods=["GET"])
def messages():
    messages = Message.query.all()
    message_list = [
        {"id": message.id, "body": message.body, "username": message.username}
        for message in messages
    ]
    return jsonify(message_list)


@app.route("/messages/<int:id>", methods=["GET"])
def messages_by_id(id):
    message = Message.query.get(id)
    if message:
        return jsonify(
            {"id": message.id, "body": message.body, "username": message.username}
        )
    else:
        return make_response(jsonify({"error": "Message not found"}), 404)


if __name__ == "__main__":
    app.run(port=5555)
