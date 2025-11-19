
create table petani(
id_petani serial PRIMARY key not null,
nama varchar(30) not null,
alamat VARCHAR(100) not null,
no_telpon varchar(14) not null,
user_name  VARCHAR(20) UNIQUE not null,
password  varchar(10) UNIQUE not null
)
CREATE table admin(
id serial PRIMARY key not null,
nama_admin varchar(50) not null,
user_name VARCHAR(20) UNIQUE not null,
password VARCHAR(10) unique not null,
no_telpon varchar(14) unique not null
)

