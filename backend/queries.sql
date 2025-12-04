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
