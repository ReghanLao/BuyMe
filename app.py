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


#registering new user
@app.route('/register', methods=['POST'])
def register():
  data = request.json
  username = data.get("username")
  password = data.get("password")

  conn = get_db_connection()
  cursor = conn.cursor()

  cursor.execute("INSERT INTO user (username, password) VALUES (%s, %s)", (username, password))
  conn.commit()

  cursor.close()
  conn.close()

  return jsonify({"message": "User registered."})


#people who submit a username and password will have their
#credentials validated 
@app.route('/login', methods=['POST'])
def login():
  #retrieve data submitted from frontend
  data = request.json 
  username = data.get("username")
  password = data.get("password")

  #TO DO (once christian set up database)
  #verify username exists in db and ensure credentials are valid
  #return json back to frontend saying whether the user is logged in or not 

  #temporary placeholder sends placeholder response back to front end
  return jsonify({
    "status": "in-progress",
    "message": "Login logic not implemented yet"
  })

if __name__ == "__main__":
  app.run()