.read lab12.sql

CREATE TABLE sp16favnum AS
  SELECT number, COUNT(*) as count FROM sp16students GROUP BY number 
    ORDER BY count DESC LIMIT 1;

CREATE TABLE sp16favpets AS
  SELECT pet, COUNT(*) as count FROM sp16students GROUP BY pet
    ORDER BY count DESC LIMIT 10;

CREATE TABLE fa16favpets AS
  SELECT pet, COUNT(*) as count FROM students GROUP BY pet
    ORDER BY count DESC LIMIT 10;

CREATE TABLE fa16dragon AS
  SELECT pet, COUNT(*) FROM students WHERE pet = 'dragon' GROUP BY pet ;

CREATE TABLE fa16alldragons AS
 SELECT pet, COUNT(*) FROM students WHERE pet LIKE '%dragon%';

CREATE TABLE obedienceimage AS
  SELECT seven, denero, COUNT(*) FROM students WHERE seven = '7' GROUP BY denero;

CREATE TABLE smallest_int_count AS
  SELECT smallest, COUNT(*) FROM students WHERE smallest > 0 GROUP BY smallest;
