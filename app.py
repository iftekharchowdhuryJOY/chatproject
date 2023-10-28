from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

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
        
        
        
        
    
    conn.close()
    # return jsonify(read_user_data)
    