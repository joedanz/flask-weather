drop table if exists weather;
create table weather (
  id integer primary key autoincrement,
  temp integer not null,
  humidity integer not null,
  zipcode text not null,
  stamp timestamp
);
