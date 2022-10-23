use buzzdash;
create table User (
name varchar(30) not null,
username varchar(30) not null,
email varchar(40) not null,
password TEXT not null,
PRIMARY KEY (username)
);

drop table if exists Request;
create table Request (
username varchar(30) not null,
date date not null,
startTime time not null,
endTime time not null,
funds varchar(30) not null,
location varchar(30) not null,
cost decimal(4,2) DEFAULT(NULL),
offer decimal(4, 2) not null,
extra text
);

drop table if exists Offer;
create table Offer (
username varchar(30) not null,
startDate date not null,
endDate date not null,
startTime time not null,
endTime time not null,
funds varchar(30) not null,
location varchar(30) not null,
cost int, 
offer decimal(4, 2) not null,
extra text
);