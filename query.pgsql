CREATE TABLE restaurant(
    name    VARCHAR(200),
    rate    FLOAT,
    review_count    FLOAT,
    type  VARCHAR(200),
    location    VARCHAR(200),
    CSS         FLOAT,
    classification  VARCHAR(10)
);
COPY restaurant(name, rate, review_count, type, location, CSS, classification) 
FROM 'D:\SnappFood\csv_files\Restaurant.csv' DELIMITER ',' CSV HEADER;

CREATE TABLE metrics_by_type(
    Restaurant_Type    VARCHAR(200),
    Average_Review    FLOAT,
    Total_Review    FLOAT,
    Average_Rating      FLOAT,
    Number  INT
);
COPY metrics_by_type(Restaurant_Type, Average_Review, Total_Review, Average_Rating, Number) 
FROM 'D:\SnappFood\csv_files\metrics_by_type.csv' DELIMITER ',' CSV HEADER;