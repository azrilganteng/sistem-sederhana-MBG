


CREATE table petani(
id_petani serial PRIMARY key not null,
nama_petani varchar(50) not null,
id_akun integer REFERENCES akun(id_akun)
)
select * from akun
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
id_panen serial PRIMARY key not null,
id_tumbuhan integer REFERENCES tumbuhan(id_tumbuhan),
id_petani integer REFERENCES petani(id_petani),
kuantitas integer not null,
tgl_panen date not null
)

CREATE table akun(
id_akun serial primary key not null,
user_name varchar(15) UNIQUE not null ,
password varchar(10) not null,
no_hp varchar(14) not null,
alamat 
id_role integer REFERENCES roles(id_role)
)

CREATE table roles(
id_role serial primary key not null,
nama_role VARCHAR(15) not null
)
CREATE TABLE pengiriman_pk(
    id_pengiriman serial PRIMARY key not null,
    id_petani integer REFERENCES petani(id_petani),
    id_karyawan integer REFERENCES karyawan(id_karyawan), 
    tgl_pengiriman date DEFAULT CURRENT_DATE,
    status_verifikasi varchar(20) DEFAULT 'sedang dikirim'
)


CREATE TABLE detail_pengiriman_pk(
    id_detail serial PRIMARY key not null,
    id_pengiriman integer REFERENCES pengiriman_pk(id_pengiriman), 
    id_panen integer REFERENCES panen(id_panen),  
    kuantitas integer not null
)

CREATE table karyawan(
id_karyawan serial PRIMARY key not null,
nama_karyawan varchar(50) not null,
alamat varchar(100) not null,
id_akun integer REFERENCES akun(id_akun)
)

CREATE TABLE gudang(
id_gudang serial PRIMARY key not null,
nama_gudang varchar(20) not null,
)

CREATE table jenis_transaksi(
id_transaksi serial PRIMARY key not null,
nama_transaksi varchar(20) not null
)

CREATE table distribusi(
id_distribusi serial primary key not null,
id_tumbuhan INTEGER REFERENCES tumbuhan(id_tumbuhan),
kuantitas integer not null,
id_gudang integer REFERENCES gudang(id_gudang),
id_karyawan integer REFERENCES karyawan(id_karyawan),
id_transaksi integer REFERENCES jenis_transaksi(id_transaksi),
tgl_distribusi date not null
)

create table detail_pengiriman_ki(
id_detail serial PRIMARY key not null,
id_tumbuhan integer REFERENCES tumbuhan(id_tumbuhan),
kuantitas integer,
id_karyawan integer REFERENCES karyawan(id_karyawan),
id_pengiriman integer REFERENCES pengiriman_ki(id_pengiriman)
)

create table pengiriman_ki(
id_pengiriman serial primary key not null,
tgl_pegiriman date not null,
status_verifikasi varchar(20) DEFAULT 'sedang dikirim',
id_dapur integer REFERENCES dapur_instansi(id_dapur)
)

create table dapur_instansi(
id_dapur serial primary key not null,
nama_dapur varchar(50) not null,
id_akun integer REFERENCES akun(id_akun)
)
select * from akun
select * from dapur_instansi

UPDATE dapur_instansi
SET id_akun = 3
WHERE id_akun =4;

