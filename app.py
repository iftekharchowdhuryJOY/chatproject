from flask import Flask, jsonify, request, render_template
import sqlite3
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = None 
    try:
        
        conn = sqlite3.connect('database.db')
    except sqlite3.Error as e:
        print(e)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/userdata', methods=["GET", "POST"])
def userdata():
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == "GET":
        cursor = conn.execute("select * from chattitleinfo")
        user_info = [dict(id=row[0], time=row[1], title=row[2], user_data=row[3], user_id=row[4])
                     for row in cursor.fetchall()
                     ]
        
        if user_info is not None:
            return jsonify(user_info)
        user_info.headers.add('Access-Control-Allow-Origin', '*')
    
        
        
    if request.method == "POST":

        title = request.form["title"]
        user_data = request.form["user_data"]
        user_id = request.form["user_id"]
        sql = """ insert into chattitleinfo (title, user_data, user_id) values (?,?,?) """
        cursor = cursor.execute(sql, (title, user_data, user_id))
        conn.commit()
        return f"user with the id: {cursor.lastrowid} created successfully"


@app.route('/userinfo', methods = ["GET", "POST"])
def userinfo():
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method== "GET":
        cursor = conn.execute("select * from userinfo")
        userdata = [dict(user_id = row[0], user_name=row[1], time=row[2])
                        for row in cursor.fetchall()
                    ]
            
        if userdata is not None:
            return jsonify(userdata)
        
    
        
    if request.method == "POST":
        
        user_id = request.form['user_id']
        user_name = request.form['user_name']
        
        sql = """ insert into userinfo (user_id, user_name) values (?,?) """
        
        cursor = cursor.execute(sql, (user_id, user_name))
        conn.commit()
        return f"user with the id: {cursor.lastrowid} created successfully"
        
        
        
@app.route("/userdata/<int:id>", methods = ["GET", "PUT", "DELETE"])

def single_user_data(id):
    
    conn = get_db_connection()
    cursor = conn.cursor()
    userdata = None 
    
    if request.method == "GET":
        
        cursor.execute("SELECT * FROM chattitleinfo where id=?", (id,))
        
        userdata = [dict(id = row[0], time=row[1], title=row[2], user_data=row[3], user_id = row[4])
                        for row in cursor.fetchall()
                    ]
       
        if userdata is not None: 
            return jsonify(userdata), 200
        else:
            return "Something wrong", 404
    
    
    if request.method == "PUT":
        sql = """ UPDATE chattitleinfo SET id=?, title=?, user_data=?, user_id=? """
        title = request.form["title"]
        userdata = request.form["user_data"]
        user_id = request.form["user_id"]
        
        updated_userdata = {"id": id, "title": title, "user_data": userdata, "user_id":user_id,}
        
        conn.execute(sql,( title,userdata, user_id))
        conn.commit()
        return jsonify(updated_userdata)
    
    
    if request.method == "DELETE":
        
        sql = """ DELETE FROM chattitleinfo WHERE id=? """
        conn.execute(sql,(id,))
        conn.commit()
        return "The user chat information with the id: {} has been deleted.".format(id), 200

    