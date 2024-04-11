import mysql.connector  
from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
     
cnx = mysql.connector.connect(user='root', host='127.0.0.1', database='fitness_center', password='passW11!')
app = Flask(__name__)
ma = Marshmallow(app)

class MemberSchema(ma.Schema):
    name = fields.String(required=True)
    class Meta: fields = ["name"]
members_schema = MemberSchema(many=True)
member_schema = MemberSchema()

class WOSessSchema(ma.Schema):
    member_id = fields.Integer(required=True)
    date = fields.Date(required=True)
    class Meta: fields = ("member_id", "date")
wk_out_sessions_schema = WOSessSchema(many=True)
wk_out_session_schema = WOSessSchema()

@app.route("/")
def home(): return "<h1>Welcome to the Fitness Center Database!</h1>"

@app.route('/members', methods=['GET'])
def get_members():
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("select * from Members")
    return cursor.fetchall()

@app.route('/members', methods=['POST'])
def add_member():
    try:
        m_data = member_schema.load(request.json)
        cursor = cnx.cursor()
        cursor.execute('insert into Members (name) values (%s)', [m_data['name']])
        cnx.commit()
        return jsonify({"message": f"Member {(m_data['name'])} added successfully!"})

    except ValidationError as err: return jsonify({"error": err.messages})

@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    try:
        cursor = cnx.cursor()
        cursor.execute('select * from Members where id = %s', [id])
        if not cursor.fetchone(): return jsonify({"ID Not Found": id})
        m_data = member_schema.load(request.json)
        updt = (m_data['name'], id)
        cursor.execute('update Members set name = %s where id = %s', updt)
        cnx.commit()
        return jsonify({"message": "Member successfully updated!"})

    except ValidationError as err: return jsonify({"error": err.messages})
    
@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    try:
        cursor = cnx.cursor()
        cursor.execute('select * from Members where id = %s', [id])
        if not cursor.fetchone(): return jsonify({"ID Not Found": id})
        cursor.execute('delete from Members where id = %s', [id])
        cnx.commit()
        return jsonify({"message": f"Member ID {id} successfully deleted!"})

    except ValidationError as err: return jsonify({"error": err.messages})

@app.route("/workouts", methods = ["GET"])
def get_workouts():
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("select * from WorkOutSessions")
    return cursor.fetchall()

@app.route("/workouts", methods = ["POST"])
def add_workout():
    try:
        w_data = wk_out_session_schema.load(request.json)
        new = (w_data['member_id'], w_data['date'])
        cursor = cnx.cursor()
        sql = 'insert into WorkOutSessions (member_id, date) values (%s,%s)'
        cursor.execute(sql, new)
        cnx.commit()
        return jsonify({"message": "Workout Session Added Successfully!"})

    except ValidationError as err: return jsonify({"error": err.messages})

@app.route('/workouts/<int:id>', methods=['PUT'])
def update_workout(id):
    try:
        cursor = cnx.cursor()
        cursor.execute('select * from WorkOutSessions where member_id = %s', [id])
        if not cursor.fetchone(): return jsonify({"ID Not Found": id})
        w_data = wk_out_session_schema.load(request.json)
        updt =  (w_data['member_id'], w_data['date'], id)
        sql = 'update WorkOutSessions set member_id = %s, date = %s where id = %s'
        cursor.execute(sql, updt)
        cnx.commit()
        return jsonify({"message": "Workout Session Updated Successfully!"})

    except ValidationError as err: return jsonify({"error": err.messages})

@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    try:
        cursor = cnx.cursor()
        cursor.execute('select * from WorkOutSessions where id = %s', [id])
        if not cursor.fetchone(): return jsonify({"ID Not Found": id})
        cursor.execute('delete from WorkOutSessions where id = %s', [id])
        cnx.commit()
        return jsonify({"message": f"Workout Session {id} Successfully Deleted!"})

    except ValidationError as err: return jsonify({"error": err.messages})

if __name__ == "__main__": app.run(debug=True)