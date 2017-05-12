.read data.sql

-- Q1
create table flight_costs as
  with price(day, pre, cur) as (
    select 3, 30, 40 union
    select day+1, cur, (pre + cur)/2 + 5 * ((day+1) % 7) from price
      where day < 25
  )
  select 1 as Day, 20 as Price union
  select 2,        30          union
  select day,      cur from price;

-- Q2
create table schedule as
  with flight_paths(path, ending, flight, cost) as (
    select departure || ", " || arrival, arrival, 1, price from flights
      where departure = "SFO" union
    select path || ", " || arrival, arrival, flight+1, cost + price
      from flight_paths, flights where ending = departure and flight < 2)
  select path, cost from flight_paths where ending = "PDX" order by cost;

-- Q3
create table shopping_cart as
  with cart(foods, last, budget) as (
    select item, price, 60 - price from supermarket where 60 - price >= 0 union
    select foods || ", " || item, price, budget - price
      from supermarket, cart where budget - price >= 0 and price >= last
  )
  select foods, budget from cart order by budget, foods;
-- Q4
create table number_of_options as
  select count(distinct meat) from main_course;

-- Q5
create table calories as
  select count(*) from main_course, pies where main_course.calories + pies.calories < 2500;

-- Q6
create table healthiest_meats as
  select meat, min(m.calories + p.calories) from main_course as m, pies as p
    group by meat having max(m.calories + p.calories) < 3000;

-- Q7
create table average_prices as
  select category, avg(MSRP) from products group by category;

-- Q8
create table lowest_prices as
  select name, store, min(price) from products, inventory
    where name = item group by name;

-- Q9
create table shopping_list as
  select p.name, store from products as p, lowest_prices as l 
    where p.name = l.name group by category having min(MSRP/rating);

-- Q10
create table total_bandwidth as
  select sum(Mbs) from shopping_list as sl, stores as s
    where s.store = sl.store;
