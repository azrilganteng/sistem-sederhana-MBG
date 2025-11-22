CREATE table petani(
id_petani serial PRIMARY key not null,
nama_petani varchar(50) not null,
alamat varchar(100) not null,
id_akun integer REFERENCES akun(id_akun)
)
select * from petani
CREATE table jenis_nutrisi(
id_nutrisi serial PRIMARY key not null,
nama_nutrisi varchar(50) not null
)
CREATE table tumbuhan(
id_tumbuhan serial PRIMARY key not null,
nama_tumbuhan VARCHAR(50) not null,
id_nutrisi INTEGER REFERENCES jenis_nutrisi(id_nutrisi)
)
CREATE table panen(
id_tumbuhan integer REFERENCES tumbuhan(id_tumbuhan),
id_petani integer REFERENCES petani(id_petani),
kuantitas integer not null,
tgl_panen date not null
)
drop table role
CREATE table karyawan(
id_karyawan serial PRIMARY key not null,
nama_karyawan varchar(50) not null,
alamat varchar(100) not null,
id_akun integer REFERENCES akun(id_akun)
)

CREATE table akun(
id_akun serial primary key not null,
user_name varchar(15) UNIQUE not null ,
password varchar(10) not null,
no_hp varchar(14) not null,
id_role integer REFERENCES roles(id_role)
)

CREATE table roles(
id_role serial primary key not null,
nama_role VARCHAR(15) not null
)
select * from akun

select 
from akun a

