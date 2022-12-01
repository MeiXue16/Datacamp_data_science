# datenmodellierung
# 新建数据库
create database 2022_01;

# 调用数据库
use 2022_01 ;

# 维度表 Create a route dimension table
CREATE TABLE route(
	route_id INTEGER PRIMARY KEY,
    park_name VARCHAR(160) NOT NULL,
    city_name VARCHAR(160) NOT NULL,
    distance_km float NOT NULL,
    route_name VARCHAR(160) NOT NULL
);
-- Create a week dimension table
CREATE TABLE week(
	week_id INTEGER PRIMARY KEY,
    week integer NOT NULL,
    month VARCHAR(160) NOT NULL,
    year integer NOT NULL
);

# 在此数据库中建表, fakten tabelle 事实表
create table if not exists running_duration(
	running_id integer primary key,
	duration_mins float not null,
    route_id INTEGER,
    week_id INTEGER ,
    FOREIGN KEY (route_id) references route(route_id),
    foreign KEY (week_id) references week(week_id)
);

# 查询2019 年 7 月的跑步分钟数
create view `duaration mins` as
SELECT 
	SUM(duration_mins) 
FROM 
	running_duration as r
INNER JOIN week as w ON r.week_id = w.week_id
WHERE w.month = 'July' and w.year = '2019';


# ALTER TABLE语句用于添加、删除或修改现有表中的列。

# ALTER TABLE语句还用于在现有表上添加和删除各种约束。

-- 对于表格fact_booksales，在名为 sales_book 的约束中，设置book_id为外键
ALTER TABLE fact_booksales ADD CONSTRAINT sales_book
    FOREIGN KEY (book_id) REFERENCES dim_book_star(book_id);
    
-- Add the time_id foreign key
ALTER TABLE fact_booksales ADD CONSTRAINT sales_time
    FOREIGN KEY (time_id) REFERENCES dim_time_star (time_id);
    
-- Add the store_id foreign key
ALTER TABLE fact_booksales ADD CONSTRAINT sales_store
    FOREIGN KEY (store_id) REFERENCES dim_store_star (store_id); 
    


-- 创建新表格Create a new table for dim_author with an author column
CREATE TABLE dim_author (
    author varchar(256)  NOT NULL
);

# 插入表记录 Insert authors 
INSERT INTO dim_author 
SELECT DISTINCT author FROM dim_book_star;

# 用 ALTER TABLE 添加一列,并将其作为主键 Add a primary key 
ALTER TABLE dim_author ADD COLUMN author_id SERIAL PRIMARY KEY;


# 用 ALTER TABLE 添加一列,并将其作为外键 Add a continent_id column with default value of 1
ALTER TABLE dim_country_sf
ADD continent_id int NOT NULL DEFAULT(1);
-- Add the foreign key constraint
ALTER TABLE dim_country_sf ADD CONSTRAINT country_continent
   FOREIGN KEY (continent_id) REFERENCES dim_continent_sf(continent_id);
   
-- Output updated table
SELECT * FROM dim_country_sf;



-- 查询 Output the new table
SELECT * FROM dim_author;

-- 查询 + 多表连接 （star schema）Output each state and their total sales_amount
SELECT s.state, sum(sales_amount)
FROM fact_booksales as f
	-- Join to get book information
    JOIN dim_book_star as b on f.book_id = b.book_id
	-- Join to get store information
    JOIN dim_store_star as s on f.store_id = s.store_id
-- Get all books with in the novel genre
WHERE  
    b.genre = 'novel'
-- Group results by state
GROUP BY
    s.state;
    

-- 查询 + 多表连接 (schneeflocken schema) Output each state and their total sales_amount
SELECT a.state, sum(sales_amount)
FROM fact_booksales as f
    -- Joins for genre
    JOIN dim_book_sf as b on f.book_id = b.book_id
    JOIN dim_genre_sf as g on b.genre_id = g.genre_id
    -- Joins for state 
    JOIN dim_store_sf as s on f.store_id = s.store_id 
    JOIN dim_city_sf as c on s.city_id = c.city_id
	JOIN dim_state_sf as a on  c.state_id = a.state_id
-- Get all books with in the novel genre and group the results by state
WHERE  
    g.genre = 'novel'
GROUP BY
    a.state;


-- 新建一张表 Create a new table to hold the cars rented by customers
CREATE TABLE cust_rentals (
  customer_id INT NOT NULL,
  car_id VARCHAR(128) NULL primary key,
  invoice_id VARCHAR(128) NULL,
  foreign key (customer_id) references customers(customer_id)
);

-- 删除原本表中冗余的列 Drop column from customers table to satisfy 1NF
ALTER TABLE customers
DROP COLUMN cars_rented,
DROP COLUMN invoice_id;



-- 新建一张表 Create a new table to satisfy 2NF
Create table cars (
  car_id VARCHAR(256) NULL,
  model VARCHAR(128),
  manufacturer VARCHAR(128),
  type_car VARCHAR(128),
  conditions VARCHAR(128),
  color VARCHAR(128)
);

-- 删除原本表中冗余的列 Drop columns in customer_rentals to satisfy 2NF
alter table customer_rentals
drop column model,
drop column manufacturer, 
drop column type_car,
drop column conditions,
drop column color;

-- 新建一张表 Create a new table to satisfy 3NF
create table car_model(
  model VARCHAR(128),
  manufacturer VARCHAR(128),
  type_car VARCHAR(128)
);

-- 删除原本表中冗余的列 Drop columns in rental_cars to satisfy 3NF
alter table rental_cars
drop column manufacturer, 
drop column type_car;

# 创建视图 (create view... + 正常的查询)
create view novel_book as 
SELECT s.state, sum(sales_amount)
FROM fact_booksales as f
	-- Join to get book information
    JOIN dim_book_star as b on f.book_id = b.book_id
	-- Join to get store information
    JOIN dim_store_star as s on f.store_id = s.store_id
-- Get all books with in the novel genre
WHERE  
    b.genre = 'novel'
-- Group results by state
GROUP BY
    s.state;

# 调用视图
select * from novel_book ;

# 查看/获取所有的视图(postgreSQL/ MySql) 两种写法应该都可以 database Views 
select * from INFORMATION_SCHEMA.views where TABLE_SCHEMA not in ('sys');
show table status where comment='view';

# 查看指定视图
SHOW CREATE VIEW `duaration mins`  ;

-- 创建视图 Create a view for reviews with a score above 9
CREATE VIEW high_scores AS
SELECT * FROM REVIEWS
WHERE score > 9;

-- 将视图作为表格进行查询 Count the number of self-released works in high_scores
SELECT COUNT(*) FROM high_scores as h
INNER JOIN labels as l ON h.reviewid =l.reviewid
WHERE l.label = 'self-released';


-- 利用两个视图创建一个新视图 Create a view with the top artists in 2017
create view top_artists_2017 as
-- with only one column holding the artist field
SELECT a.artist FROM top_15_2017 as t
INNER JOIN artist_title as a
ON t.reviewid = a.reviewid;

-- Output the new view
SELECT * FROM top_artists_2017;

# 删除视图以及所有依赖于它的视图
drop view top_15_2017 cascade ;


-- 撤销所有用户对于视图long_reviews的更新和插入权限 Revoke everyone's update and insert privileges
REVOKE update,insert on long_reviews FROM public; 

-- 授予editor对于视图long_reviews的更新和插入权限 Grant the editor update and insert privileges 
GRANT update,insert on long_reviews TO editor; 

-- 重新定义一个视图（列名需要与之前保持一致，多出来的列放在最后）Redefine the artist_title view to have a label column
create or replace view artist_title AS
SELECT reviews.reviewid, reviews.title, artists.artist, labels.label
FROM reviews
INNER JOIN artists
ON artists.reviewid = reviews.reviewid
INNER JOIN labels
ON labels.reviewid = reviews.reviewid;

SELECT * FROM artist_title;

# 创建物化视图（保存查询结果的视图）,仅适用于 postgreSQL
# create MATERIALIZED view my_mv as select * from table1 ;
# refresh MATERIALIZED view my_mv;

-- 创建物化视图Create a materialized view called genre_count 
# create materialized view genre_count as 
SELECT genre, COUNT(*) 
FROM genres
GROUP BY genre;

# 插入值
INSERT INTO genres
VALUES (50000, 'classical');

-- 更新物化视图 Refresh genre_count
# refresh materialized view genre_count;

# SELECT * FROM genre_count;

# 创建数据库中的角色(group role)，和访问权限
create role data_analyst;
create role data_scientist;
-- intern (user role)
-- create ROLE intern WITH password 'passwordForIntern' valid until '2022-12-30';
-- create role admin CREATEDB;
-- alter role admin CREATEROLE ;
-- create role intern login; 
# 创建角色admin 带有CREATEDB 和CREATEROLE权限
-- create role admin with CREATEDB CREATEROLE;

# 授予data_analyst 2022_01和hrs数据库中所有表格的更新和插入的权限
grant update,insert on 2022_01.* to data_analyst ;
grant update,insert on hrs.* to data_analyst ;

# 授予权限
-- Grant data_scientist update and insert privileges
grant update,insert ON long_reviews TO data_scientist;

-- Give Marta's role a password
-- alter role marta with password 's3cur3p@ssw0rd';

#撤销权限
revoke update on hrs.tb_dept from data_analyst ;

# 将用户角色intern添加到 组角色data_analyst中
grant data_analyst to intern; 

# 撤销用户角色
revoke data_analyst from intern ;


-- 表格垂直分区 vertical  partition : Create a new table called film_descriptions
CREATE TABLE film_descriptions (
    film_id INT,
    long_description TEXT
);

-- Copy the descriptions from the film table
INSERT INTO film_descriptions
SELECT film_id, long_description FROM film;
    
-- Drop the descriptions from the original table
alter table film drop column long_description;

-- Join to view the original table
SELECT * FROM film
JOIN film_descriptions USING(film_id);

# 

-- 创建水平分区 （postgreSQL）Create a new table called film_partitioned
-- CREATE TABLE film_partitioned (
--   film_id INT,
--   title TEXT NOT NULL,
--   release_year TEXT
-- )
-- PARTITION BY LIST (release_year)  #  也可以 PARTITION BY range/key  (...)
-- PARTITIONS 3;  

-- -- Create the partitions for 2019, 2018, and 2017
-- CREATE TABLE film_2019
-- 	PARTITION OF film_partitioned FOR VALUES IN ('2019');

-- CREATE TABLE film_2018
-- 	PARTITION OF film_partitioned FOR VALUES IN ('2018');

-- CREATE TABLE film_2017
-- 	PARTITION OF film_partitioned FOR VALUES IN ('2017');

-- -- Insert the data into film_partitioned
-- INSERT INTO film_partitioned
-- SELECT film_id, title, release_year FROM film;

-- -- View film_partitioned
-- SELECT * FROM film_partitioned;

# 创建水平分区 MySQL
CREATE TABLE members (
    firstname VARCHAR(25) NOT NULL,
    lastname VARCHAR(25) NOT NULL,
    username VARCHAR(16) NOT NULL,
    email VARCHAR(35),
    joined DATE NOT NULL
)
PARTITION BY KEY(joined)
PARTITIONS 6;

# 创建水平分区
CREATE TABLE members (
    firstname VARCHAR(25) NOT NULL,
    lastname VARCHAR(25) NOT NULL,
    username VARCHAR(16) NOT NULL,
    email VARCHAR(35),
    joined DATE NOT NULL
)
PARTITION BY RANGE( YEAR(joined) ) (
    PARTITION p0 VALUES LESS THAN (1960),
    PARTITION p1 VALUES LESS THAN (1970),
    PARTITION p2 VALUES LESS THAN (1980),
    PARTITION p3 VALUES LESS THAN (1990),
    PARTITION p4 VALUES LESS THAN MAXVALUE
);

 CREATE TABLE t2 (val INT)
    PARTITION BY LIST(val)(
    PARTITION mypart1 VALUES IN (1,3,5),
    PARTITION myPart2 VALUES IN (2,4,6)
    );