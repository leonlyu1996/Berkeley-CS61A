create table parents as
  select "abraham" as parent, "barack" as child union
  select "abraham"          , "clinton"         union
  select "delano"           , "herbert"         union
  select "fillmore"         , "abraham"         union
  select "fillmore"         , "delano"          union
  select "fillmore"         , "grover"          union
  select "eisenhower"       , "fillmore";

create table dogs as
  select "abraham" as name, "long" as fur, 26 as height union
  select "barack"         , "short"      , 52           union
  select "clinton"        , "long"       , 47           union
  select "delano"         , "long"       , 46           union
  select "eisenhower"     , "short"      , 35           union
  select "fillmore"       , "curly"      , 32           union
  select "grover"         , "short"      , 28           union
  select "herbert"        , "curly"      , 31;

create table sizes as
  select "toy" as size, 24 as min, 28 as max union
  select "mini",        28,        35        union
  select "medium",      35,        45        union
  select "standard",    45,        60;

-------------------------------------------------------------
-- PLEASE DO NOT CHANGE ANY SQL STATEMENTS ABOVE THIS LINE --
-------------------------------------------------------------

-- The size of each dog
create table size_of_dogs as
  select name, size from dogs, sizes where height > min and height <= max;

-- All dogs with parents ordered by decreasing height of their parent
create table by_height as
  select child from parents, dogs where name = parent order by height desc;

-- Sentences about siblings that are the same size
create table sentences as
  with siblings(a, b) as (
    select x.child, y.child from parents as x, parents as y 
      where x.parent = y.parent and x.child < y.child)
  select a || " and " || b || " are " || s1.size || " siblings" from siblings, 
    size_of_dogs as s1, size_of_dogs as s2 where a = s1.name and b = s2.name and s1.size = s2.size;

-- Ways to stack 4 dogs to a height of at least 170, ordered by total height
create table stacks as
  select d1.name || ", " || d2.name || ", " || d3.name || ", " || d4.name, 
    d1.height + d2.height + d3.height + d4.height as sum_height
  from dogs as d1, dogs as d2, dogs as d3, dogs as d4 where d2.height > d1.height
  and d3.height > d2.height and d4.height > d3.height 
  and sum_height >= 170 order by sum_height;

-- non_parents is an optional, but recommended question
-- All non-parent relations ordered by height difference
create table non_parents as
  with 
    grandparents(grandparent, grandchild) as (
      select p.parent, c.child from parents as p, parents as c where p.child = c.parent),
    super_parents(a, b) as (
      select grandparent, grandchild from grandparents union
      select grandchild, grandparent from grandparents union
      select grandparent, child from grandparents, parents where grandparents.grandchild = parents.parent union
      select child, grandparent from grandparents, parents where grandparents.grandchild = parents.parent union
      select parent, grandchild from grandparents, parents where grandparents.grandparent = parents.child union
      select grandchild, parent from grandparents, parents where grandparents.grandparent = parents.child
    )
  select a, b from super_parents, dogs as d1, dogs as d2 where a = d1.name and b = d2.name 
    order by d1.height - d2.height;

create table ints as
    with i(n) as (
        select 1 union
        select n+1 from i limit 100
    )
    select n from i;

create table divisors as
    with charts(x, y, z) as (
      select a.n, b.n, a.n * b.n from ints as a, ints as b where a.n * b.n <= 100
    )
    select z as n, count(*) as count from charts group by z;

create table primes as
    select n from divisors where count = 2;
