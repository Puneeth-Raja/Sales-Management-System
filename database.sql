create database Sales_Intelligence_Hub;
use Sales_Intelligence_Hub;

create table branches(
branch_id int auto_increment primary key,
branch_name varchar(100),
branch_admin_name varchar(100)
);

create table users(
user_id int primary key auto_increment,
username varchar(100),
`password` varchar(255),
branch_id int,
role enum('Super Admin','Admin'),
email varchar(255) unique,
KEY(branch_id),
foreign key(branch_id) references branches(branch_id)
);



create table customer_sales(
sale_id int primary key auto_increment,
branch_id int,
joining_date Date,
customer_name varchar(100),
mobile_number Varchar(15),
product_name varchar(30),
gross_sales decimal(12,2),
received_amount decimal(12,2),
pending_amount decimal(12,2) generated always as (gross_sales - received_amount) stored,
`status` ENUM('Open','Close'),
KEY(branch_id),
foreign key(branch_id) references branches(branch_id)
);

ALTER TABLE customer_sales
ADD UNIQUE (mobile_number);

create table payment_splits(
payment_id int primary key auto_increment,
sale_id int,
payment_date Date,
amount_paid decimal(12,2),
payment_method varchar(50),
KEY(sale_id),
foreign key(sale_id) references customer_sales(sale_id)
);

DELIMITER $$
create trigger trg_payment_insert
after insert on payment_splits
FOR EACH ROW
BEGIN
UPDATE customer_sales
SET received_amount = (select coalesce(sum(amount_paid),0) from payment_splits where sale_id=NEW.sale_id)
where sale_id=NEW.sale_id;
END $$
DELIMITER ;

