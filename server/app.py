from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    new_message = Message(
        body=data.get('body'),
        username=data.get('username')
    )
    db.session.add(new_message)
    db.session.commit()
    return jsonify({
        "id": new_message.id,
        "body": new_message.body,
        "username": new_message.username,
        "created_at": new_message.created_at.isoformat() if new_message.created_at else None
    }), 201

@app.route('/messages')
def messages():
    messages = Message.query.all()
    messages_list = [
        {
            "id": message.id,
            "body": message.body,
            "username": message.username,
            "created_at": message.created_at.isoformat() if message.created_at else None
        }
        for message in messages
    ]
    return jsonify(messages_list)

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get_or_404(id)
    data = request.get_json()
    if "body" in data:
        message.body = data["body"]
    if "username" in data:
        message.username = data["username"]
    db.session.commit()
    return jsonify({
        "id": message.id,
        "body": message.body,
        "username": message.username,
        "created_at": message.created_at.isoformat() if message.created_at else None
    })

if __name__ == '__main__':
    app.run(port=5555)
