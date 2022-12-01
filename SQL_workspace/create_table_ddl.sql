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


