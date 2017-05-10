.read sp16data.sql
.read fa16data.sql

CREATE TABLE obedience AS
  SELECT seven, denero FROM students;

CREATE TABLE smallest_int AS
  SELECT time, smallest FROM students WHERE smallest > 8 ORDER BY smallest LIMIT 20;

CREATE TABLE greatstudents AS
  SELECT fa.date, fa.number, fa.pet, fa.color, sp.color FROM students AS fa, sp16students AS sp
    WHERE fa.date = sp.date AND fa.number = sp.number AND sp.pet = fa.pet;

CREATE TABLE sevens AS
  SELECT a.seven FROM students AS a, checkboxes AS b 
    WHERE a.time = b.time AND a.number = 7 AND b.'7' = 'True';

CREATE TABLE matchmaker AS
  SELECT a.pet, a.song, a.color, b.color FROM students AS a, students AS b
    WHERE a.pet = b.pet AND a.song = b.song AND a.time < b.time