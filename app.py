from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

#sets up flask app and allows frontend to communicate with backend
app = Flask(__name__)
CORS(app)

db_config = {
  'host': 'localhost',
  'user': 'root',
  'password': '9pJJBAsql',
  'database': 'cs336project'
}

def get_db_connection():
  return mysql.connector.connect(**db_config)

@app.route('/')
def home():
  return 'testing'

#people who submit a username and password will have their
#credentials validated 
@app.route('/login', methods=['POST'])
def login():
  #retrieve data submitted from frontend
  data = request.json 
  username = data.get("username")
  password = data.get("password")

  conn = get_db_connection()
  cursor = conn.cursor(dictionary=True)

  cursor.execute("SELECT * FROM user WHERE username = %s AND password = %s", (username, password))
  user = cursor.fetchone()

  cursor.close()
  conn.close()

  #TO DO (once christian set up database)
  #verify username exists in db and ensure credentials are valid
  #return json back to frontend saying whether the user is logged in or not
  if user:
    return jsonify({"message": f"Hello, {user['username']}."})
  else:
    return jsonify({"message": "Invalid username or password"})

if __name__ == "__main__":
  app.run()