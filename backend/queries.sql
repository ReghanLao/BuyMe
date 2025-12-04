CREATE TABLE item (
  iid        INT AUTO_INCREMENT PRIMARY KEY,
  seller_id  INT NOT NULL,
  name       VARCHAR(255) NOT NULL,
  item_type  ENUM('shoes','shirts','pants') NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (seller_id) REFERENCES user(uid)
);


CREATE TABLE shoes (
  iid INT PRIMARY KEY,
  size        INT NOT NULL,   
  gender      ENUM('mens','womens','unisex') NOT NULL,
  material    VARCHAR(100),
  color       VARCHAR(100),
  brand       VARCHAR(100),
  condition   ENUM('new','used') NOT NULL,
  FOREIGN KEY (iid) REFERENCES item(iid)
);

CREATE TABLE shirts (
  iid INT PRIMARY KEY,
  size        ENUM('XS','S','M','L','XL','XXL') NOT NULL,
  sleeve_type ENUM('short','long','sleeveless'),
  material    VARCHAR(100),
  color       VARCHAR(100),
  brand       VARCHAR(100),
  FOREIGN KEY (iid) REFERENCES item(iid)
);

CREATE TABLE pants (
  iid INT PRIMARY KEY,
  waist       INT NOT NULL,
  material    VARCHAR(100),
  color       VARCHAR(100),
  brand       VARCHAR(100),
  FOREIGN KEY (iid) REFERENCES item(iid)
);

CREATE TABLE auction (
  auction_id      INT AUTO_INCREMENT PRIMARY KEY,

  item_id         INT NOT NULL,
  seller_id       INT NOT NULL,

  initial_price   DECIMAL(10,2) NOT NULL,
  min_sell_price  DECIMAL(10,2) NOT NULL,
  bid_increment   DECIMAL(10,2) NOT NULL,

  start_time      DATETIME NOT NULL,
  end_time        DATETIME NOT NULL,

  status          ENUM('scheduled','running','closed') NOT NULL DEFAULT 'scheduled',

  current_price   DECIMAL(10,2) NOT NULL,
  winner_id       INT NULL,

  FOREIGN KEY (item_id) REFERENCES item(iid),

  FOREIGN KEY (seller_id) REFERENCES user(uid),

  FOREIGN KEY (winner_id) REFERENCES user(uid),
);

CREATE TABLE bid (
  bid_id       INT AUTO_INCREMENT PRIMARY KEY,
  auction_id   INT NOT NULL,
  bidder_id    INT NOT NULL,
  amount       DECIMAL(10,2) NOT NULL,
  created_at   DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (auction_id) REFERENCES auction(auction_id),
  FOREIGN KEY (bidder_id)  REFERENCES user(uid),
);
