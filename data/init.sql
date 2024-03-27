CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255),
    opinions_count INTEGER,
    average_mark FLOAT(3,2)
);

CREATE TABLE IF NOT EXISTS opinions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    author VARCHAR(255),
    recommendation VARCHAR(255),
    stars  FLOAT(3,2),
    is_opinion_confirmed_by_purchase BOOLEAN,
    date_of_opinion DATETIME,
    date_of_purchase DATETIME,
    likes INTEGER,
    dislikes INTEGER,
    content TEXT,
    FOREIGN KEY(product_id) REFERENCES products(id)
);

CREATE TABLE IF NOT EXISTS features (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    opinion_id INTEGER,
    product_id INTEGER,
    name VARCHAR(255),
    is_positive BOOLEAN,
    FOREIGN KEY(opinion_id) REFERENCES opinions(id),
    FOREIGN KEY(product_id) REFERENCES products(id)
);
