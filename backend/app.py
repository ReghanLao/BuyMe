from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

#sets up flask app and allows frontend to communicate with backend
app = Flask(__name__)
CORS(app)

db_config = {
  'host': DB_HOST,
  'user': DB_USER,
  'password': DB_PASSWORD,
  'database': DB_NAME
}

def get_db_connection():
  return mysql.connector.connect(**db_config)

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
    return jsonify({"message": "Invalid username or password"}), 401

@app.route('/api/auctions', methods=['POST'])
def create_auction():
  data = request.json 

  seller_id = data.get("seller_id")
  name = data.get("name")
  item_type = data.get("item_type")
  item_details = data.get("item_details")

  initial_price = data.get("initial_price")
  min_sell_price = data.get("min_sell_price")
  bid_increment = data.get("bid_increment")
  start_time = data.get("start_time")
  end_time = data.get("end_time")

  conn = get_db_connection()
  cursor = conn.cursor()

  #inserting into main item table 
  cursor.execute("""
    INSERT INTO item (seller_id, name, item_type)
    VALUES (%s, %s, %s)
                 """, (seller_id, name, item_type))
  
  item_id = cursor.lastrowid

  #inserting into subtypes 
  if item_type == "shoes":
    cursor.execute("""
      INSERT INTO shoes (iid, size, gender, material, color, brand, condition)
      VALUES (%s, %s, %s, %s, %s, %s, %s)
                   """, (item_id, 
                         item_details.get("size"), 
                         item_details.get("gender"),
                         item_details.get("material").
                         item_details.get("color"),
                         item_details.get("brand"),
                         item_details.get("condition")
                         ))
  elif item_type == "shirts":
    cursor.execute("""
      INSERT into shirts (iid, size, sleeve_type, material, color, brand)
      VALUES (%s, %s, %s, %s, %s, %s)
                   """, (item_id, 
                      item_details.get("size"),
                      item_details.get("sleeve_type"),
                      item_details.get("material"),
                      item_details.get("color"),
                      item_details.get("brand")
                      ))
  elif item_type == "pants":
    cursor.execute("""
      INSERT INTO pants (iid, waist, material, color, brand)
      VALUES (%s, %s, %s, %s, %s)
                  """, (
                    item_id, 
                    item_details.get("waist"),
                    item_details.get("material"),
                    item_details.get("color"),
                    item_details.get("brand")
                  ))
    
  #insert into auction 
  #current price is initial price to begin with 
  cursor.execute("""
    INSERT INTO auction (item_id, seller_id, initial_price, min_sell_price, bid_increment, start_time, end_time, current_price)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                """, (
                  item_id, 
                  seller_id, 
                  initial_price,
                  min_sell_price,
                  bid_increment,
                  start_time,
                  end_time,
                  initial_price
                ))
  auction_id = cursor.lastrowid

  conn.commit()
  cursor.close()
  conn.close()

  return jsonify({
    "message": "Auction created successfully",
    "auction_id": auction_id,
    "item_id": item_id
  })

if __name__ == "__main__":
  app.run()