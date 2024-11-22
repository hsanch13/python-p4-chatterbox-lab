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

@app.route('/messages', methods=["GET", "POST"])
def messages():
    try:
        if request.method == "GET":
            #! how do I query all message OBJECTS
            messages = Message.query
            #! what can I return?
            return make_response([message_obj.to_dict() for message_obj in messages], 200)
        else: 
            #! 1. Retrieve data from the request body (JSON)
            data = request.get_json()
            #! 2. Instantiate a message object (use Message) and pass the info along
            new_message = Message(body=data.get("body", "default text"), username=data.get("username"))
            #! 3. Don't forget to add the new object to the session for tracking (and automatic SQL statement creation)
            db.session.add(new_message)
            #! 4. Commit the session to fire those SQL statements
            db.session.commit()
            #! return what you created!!!
            return make_response(jsonify(new_message.to_dict()), 201)
    except Exception as e:
        return make_response({"error": str(e)}), 400

@app.route('/messages/<int:id>', methods=["PATCH", "DELETE"])
def messages_by_id(id):
    message = db.session.get_one(Message, id)
    try:
        if request.method == "PATCH":
            data = request.get_json()["body"]
            message.body = data
            db.session.add(message)
            db.session.commit()
            return make_response(message.to_dict(), 200)
        elif request.method == "DELETE":
            db.session.delete(message)
            db.session.commit()
            response_body = {
                "delete_successful": True,
                "message": "Message deleted."
            }
            return make_response(response_body, 200)
    except Exception as e:
        return make_response({"error": str(e)}), 400

    #try: 
        #1. TRY to find a production with the ID provided
        # production = db.session.get(Production, id)
        #2. IF FOUND: db.session.delete(object_var_found) -> db.session.commit()
        # if production:
            # db.session.delete(production)
            # db.session.commit()
            # return make_response("", 204)
        #3. IF NOT FOUND: return an error in good structure for React app -> {"error": "I couldn't find a xyz {}"}
         # else:
         #      return make_response(
         #          {"error": f"I could not fund the production with ID {id}"}, 404
         #      ) 
    #except Exception as e:
        # return {"error": str(e), 400
if __name__ == '__main__':
    app.run(port=5555)
