-- Insert a new shoe item with its shoe-specific attributes.
INSERT INTO shoes (iid, size, gender, material, color, brand, condition)
VALUES (?, ?, ?, ?, ?, ?, ?);

-- Insert a new shirt item with its shirt-specific attributes.
INSERT INTO shirts (iid, size, sleeve_type, material, color, brand)
VALUES (?, ?, ?, ?, ?, ?);

-- Insert a new pants item with its pants-specific attributes.
INSERT INTO pants (iid, waist, material, color, brand)
VALUES (?, ?, ?, ?, ?);

-- Mark an auction as closed and store the winner and final sale price.
UPDATE auction
SET status = 'closed',
    winner_id = ?,
    current_price = ?
WHERE auction_id = ?;

-- Get the highest bid (and its bidder) for a specific auction.
SELECT bidder_id, amount
FROM bid
WHERE auction_id = ?
ORDER BY amount DESC, created_at ASC
LIMIT 1;

-- Retrieve all currently active auctions that are within their running time window.
SELECT a.*, i.name
FROM auction a
JOIN item i ON a.item_id = i.iid
WHERE a.status = 'running'
  AND NOW() BETWEEN a.start_time AND a.end_time;

-- Search active shoe auctions filtered by price range.
SELECT a.*, i.name
FROM auction a
JOIN item i ON a.item_id = i.iid
WHERE a.status = 'running'
  AND i.item_type = 'shoes'
  AND a.current_price BETWEEN ? AND ?;

-- Search active shoe auctions matching gender, size, and color filters.
SELECT a.*, i.name, s.size, s.gender, s.color
FROM auction a
JOIN item i   ON a.item_id = i.iid
JOIN shoes s  ON s.iid = i.iid
WHERE a.status = 'running'
  AND s.gender = ?
  AND s.size = ?
  AND s.color = ?;

-- Retrieve auction info needed to validate a new bid.
SELECT current_price, bid_increment, status
FROM auction
WHERE auction_id = ?;

-- Insert a new bid placed by a user on an auction.
INSERT INTO bid (auction_id, bidder_id, amount)
VALUES (?, ?, ?);

-- Update the auction's current highest bid and leader.
UPDATE auction
SET current_price = ?,
    winner_id = ?
WHERE auction_id = ?;

-- Get full bid history for an auction, including bidder usernames.
SELECT b.amount, b.created_at, u.username
FROM bid b
JOIN user u ON b.bidder_id = u.uid
WHERE b.auction_id = ?
ORDER BY b.created_at ASC;

-- Get all auctions a user has participated in as a bidder.
SELECT DISTINCT a.*
FROM auction a
JOIN bid b ON b.auction_id = a.auction_id
WHERE b.bidder_id = ?;

-- Get all auctions created by a particular seller.
SELECT *
FROM auction
WHERE seller_id = ?;
