from flask import Flask, request, jsonify

app = Flask(__name__)

# A simple in-memory data store as a list of dictionaries
reminders = [
    {
        "id": 1,
        "title": "Team Meeting at 3PM Today",
        "description": "",
        "remind_at": "2023-07-28T15:00:00"
    },
    {
        "id": 2,
        "title": "Call Jack Tomorrow at 10AM",
        "description": "Call Jack regarding the project's release date",
        "remind_at": "2023-07-29T10:00:00"
    },
]


@app.route('/reminders', methods=['GET'])
def get_reminders():
    return jsonify(reminders)


@app.route('/reminder/<int:reminder_id>', methods=['GET'])
def get_reminder(reminder_id):
    reminder = next((reminder for reminder in reminders if reminder['id'] == reminder_id), None)
    if reminder:
        return jsonify(reminder)
    else:
        return jsonify({"message": "Reminder not found"}), 404


@app.route('/reminders', methods=['POST'])
def create_reminder():
    if not request.json or 'title' not in request.json or 'description' not in request.json or \
            'remind_at' not in request.json:
        return jsonify({
            "message": "Invalid data"
        }), 400

    new_reminder = {
        "id": len(reminders) + 1,
        "title": request.json['title'],
        "description": request.json['description'],
        "remind_at": "2023-07-28T15:00:00"
    }

    reminders.append(new_reminder)
    return jsonify(new_reminder), 201


@app.route('/reminders/<int:reminder_id>', methods=['PUT'])
def update_reminder(reminder_id):
    reminder = next((reminder for reminder in reminders if reminder['id'] == reminder_id), None)
    if not reminder:
        return jsonify({"message": "Reminder not found"}), 404

    if not request.json or 'title' not in request.json or 'description' not in request.json or \
            'remind_at' not in request.json:
        return jsonify({"message": "Invalid data"}), 400

    reminder['title'] = request.json['title']
    reminder['description'] = request.json['description']
    return jsonify(reminder)


@app.route('/reminders/<int:reminder_id>', methods=['DELETE'])
def delete_reminder(reminder_id):
    global reminders
    reminders = [reminder for reminder in reminders if reminder['id'] != reminder_id]
    return jsonify({"message": "Reminder deleted successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True)
