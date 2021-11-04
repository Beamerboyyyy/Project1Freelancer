If you are using phpmyadmin deactivate Mysql80 service from services(if you have installed mysql) then open phpmyadmin localhost page. Write following sql queries in SQL tab and run them one by one by pressing 'GO':
1. CREATE database 'walmart'
2. USE walmart
CREATE TABLE `Items` (
  `id` int(11) NOT NULL,
  `item_number` varchar(11) NOT NULL PRIMARY KEY,
  `product_title` text,
  `product_url` text,
  `image_url` text,
  `price` float NOT NULL,
  `updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `alerted` int(11) DEFAULT NULL,
  `price_history` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
3. USE walmart
CREATE TABLE `urls` (
  `id` int(11) NOT NULL,
  `url` text NOT NULL,
  `category` varchar(600) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
------------------------------------------------------------------------------------------------------------
1. Move to the project directory by cmd and install requirements by pip install requirements.txt to get all the necessary packages used.
2. Change your hostname,username and password from the python script named 'client_final.py' to whatever your mysql connection have or just make the local connection with username 'root' and password 'owaisahmed123'.
3. Before starting program make run the sql queries in the url_db.sql and items.sql respectively.
4. Make sure you are using database named 'Walmart'.
5. If captcha occurs, just use vpn to any region. I have almost elminated the captchas but if in case captcha blocks the working of algorithm contact me again.
6. The primary key of items.sql is set for item_id attribute that is walmart_item_id in py script. The program updates the items in items.sql if its item_id attribute is same otherwise the item is updated.
7. The program will automatically start scrapping from the first link of urls table.
---------------------------------------------Thanks-------------------------------------------------------- 