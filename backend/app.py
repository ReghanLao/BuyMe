import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
from decimal import Decimal
from items import items_bp


#sets up flask app and allows frontend to communicate with backend
app = Flask(__name__)
CORS(app)
app.register_blueprint(items_bp)


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
                         item_details.get("material"),
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

#helper function - simple notification insert
def create_notification(cursor, user_id, auction_id, message):
    cursor.execute(
        "INSERT INTO notification (user_id, auction_id, message) VALUES (%s, %s, %s)",
        (user_id, auction_id, message))

#lets user place a manual bid 
@app.route('/api/auctions/<int:auction_id>/bid', methods=['POST'])
def place_bid(auction_id):
  data = request.json or {} #incase req body isn't valid json 
  bidder_id = data.get('bidder_id')
  amount = data.get('amount')

  if bidder_id is None or amount is None:
    return jsonify({'error':'missing bidder_id or amount'}), 400
  
  #convert amount to decimal
  try:
    amount = Decimal(str(amount))
  except Exception:
    return jsonify({'error':'invalid amount'}), 400
  
  conn = get_db_connection()
  cursor = conn.cursor(dictionary=True)

  try:
    conn.start_transaction()

    cursor.execute(
        """
        SELECT auction_id, current_price, bid_increment, end_time, status,
              min_sell_price, seller_id
        FROM auction
        WHERE auction_id = %s
        FOR UPDATE
        """,
        (auction_id,)
    )

    auction = cursor.fetchone()

    #if any errors fetching auction then rollback transaction aka release lock 
    if not auction:
      conn.rollback()
      return jsonify({'error':'could not find auction'}), 404

    if auction['status'] != 'running':
      conn.rollback()
      return jsonify({'error':'auction not running'}), 400

    if auction['end_time'] and auction['end_time'] <= datetime.utcnow():
      conn.rollback()
      return jsonify({'error':'auction already ended'}), 400

    current_price = Decimal(str(auction['current_price']))
    bid_increment = Decimal(str(auction['bid_increment']))

    min_required = current_price + bid_increment
    if amount < min_required:
      conn.rollback()
      return jsonify({'error':f'Bid is too low! Minimum required {min_required}'}), 400
    
    #insert the manual bid if valid 
    cursor.execute(
        "INSERT INTO bid (auction_id, bidder_id, amount) VALUES (%s,%s,%s)",
        (auction_id, bidder_id, str(amount)))
    new_bid_id = cursor.lastrowid

    #update the auction's new price to be current price and the "current winner"
    cursor.execute(
            "UPDATE auction SET current_price = %s, winner_id = %s WHERE auction_id = %s",
            (str(amount), bidder_id, auction_id))
    
    #let autobids react 
    ## TO BE IMPLEMENTED
    #resolve_autobids_simple(conn, cursor, auction_id)
    
    #fetch final current_price and final current winner
    cursor.execute("SELECT current_price, winner_id FROM auction WHERE auction_id = %s", (auction_id,))
    final = cursor.fetchone()

    #notify other bidders that they were outbid 
    #gets all other bidders in the same auction as the winner so far
    cursor.execute(
      "SELECT DISTINCT bidder_id FROM bid WHERE auction_id = %s AND bidder_id != %s",
      (auction_id, final['winner_id']))
    
    rows = cursor.fetchall()
    msg = f"A higher bid of {final['current_price']} has been placed on auction {auction_id}."
    for row in rows:
      create_notification(cursor, row['bidder_id'], auction_id, msg)

    #commit transaction
    conn.commit()

    #updates front end
    return jsonify({
      'message':'bid was placed',
      'bid_id': new_bid_id,
      'current_price': final['current_price'],
      'winner_id': final['winner_id']
    })
  except: 
    conn.rollback()
    return jsonify({'error':'internal error'}), 500
  finally:
    cursor.close()
    conn.close()

#allows users to post their max autobid 
@app.route('/api/auctions/<int:auction_id>/autobid', methods=['POST'])
def set_autobid(auction_id):
  data = request.json or {} #incase req body isn't valid json 
  bidder_id = data.get('bidder_id')
  max_bid = data.get('max_bid')

  if bidder_id is None or max_bid is None:
    return jsonify({'error': 'missing fields either bidder id or max bid'}), 400
  
  try: 
    max_bid = Decimal(str((max_bid)))
  except:
    return jsonify({'error': 'invalid max bid'}), 400

  conn = get_db_connection()
  cursor = conn.cursor(dictionary=True)

  try:
    conn.start_transaction()
    #check auction exists and is running
    #want to set lock on auction row so that no other transaction can modify it 
    cursor.execute("SELECT auction_id, current_price, status FROM auction WHERE auction_id = %s FOR UPDATE", (auction_id,))
    auction = cursor.fetchone()
    if not auction:
      conn.rollback()
      return jsonify({'error':'auction was not found'}), 404
    if auction['status'] != 'running':
      conn.rollback()
      return jsonify({'error':'auction is not running'}), 400
    
    #now we want to update / insert the autobid 
    
  except:





#fetch bid history for a particular auction ordered by earliest to latest
@app.route('/api/auctions/<int:auction_id>/bids', methods=['GET'])
def get_bid_history(auction_id):
  conn = get_db_connection()
  cursor = conn.cursor(dictionary=True)

  try:
    cursor.execute("SELECT bid_id, bidder_id, amount, created_at FROM bid WHERE auction_id = %s ORDER BY created_at ASC", (auction_id))
    rows = cursor.fetchall()
    return jsonify({'bids': rows})
  finally: 
    cursor.close()
    conn.close()

if __name__ == "__main__":
  app.run()