# items.py
import mysql.connector
from flask import Blueprint, request, jsonify
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

# local DB helper (you can later refactor this into a shared db.py)
db_config = {
    "host": DB_HOST,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "database": DB_NAME,
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

items_bp = Blueprint("items", __name__)

@items_bp.route("/api/items", methods=["GET"])
def browse_items():
    """
    Browse/search items and see their current auction status & price.
    Supports filters: item_type, min_price, max_price, keyword, sort_by, sort_dir.
    """

    # Query params from frontend
    item_type = request.args.get("item_type")          # shoes | shirts | pants | ""
    min_price = request.args.get("min_price", type=float)
    max_price = request.args.get("max_price", type=float)
    keyword   = request.args.get("keyword")            # search in item name
    sort_by   = request.args.get("sort_by", "end_time")
    sort_dir  = request.args.get("sort_dir", "asc")

    # We’ll default to showing only currently running auctions
    status = "running"

    # Build base query
    query = """
        SELECT
            a.auction_id,
            a.status,
            a.current_price,
            a.initial_price,
            a.end_time,
            i.iid,
            i.name,
            i.item_type
        FROM auction a
        JOIN item i ON a.item_id = i.iid
        WHERE 1 = 1
    """
    params = []

    # Only running auctions by default, and within their time window
    if status:
        query += " AND a.status = %s"
        params.append(status)
        query += " AND NOW() BETWEEN a.start_time AND a.end_time"

    # Optional filters
    if item_type:
        query += " AND i.item_type = %s"
        params.append(item_type)

    if min_price is not None:
        query += " AND a.current_price >= %s"
        params.append(min_price)

    if max_price is not None:
        query += " AND a.current_price <= %s"
        params.append(max_price)

    if keyword:
        # simple name match; you can later extend to brand/color/etc.
        query += " AND i.name LIKE %s"
        params.append(f"%{keyword}%")

    # Prevent SQL injection by whitelisting sort columns
    allowed_sort_by = {
        "end_time": "a.end_time",
        "current_price": "a.current_price",
        "name": "i.name",
    }
    sort_column = allowed_sort_by.get(sort_by, "a.end_time")
    sort_direction = "DESC" if sort_dir == "desc" else "ASC"

    query += f" ORDER BY {sort_column} {sort_direction}"

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(query, params)
        rows = cursor.fetchall()
    except Exception as e:
        print("Error in /api/items:", e)
        cursor.close()
        conn.close()
        return jsonify({"message": "Internal server error"}), 500

    cursor.close()
    conn.close()

    # Frontend expects { items: [...] }
    return jsonify({"items": rows})
