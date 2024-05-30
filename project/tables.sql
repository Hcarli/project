CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    hash TEXT
);

CREATE TABLE address (
    name TEXT,
    email TEXT,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE countries (
    id INTEGER PRIMARY KEY,
    countrycode TEXT,
    country TEXT,
    currency TEXT

);

CREATE TABLE pennworld (
    economic_id INTEGER,
    year INTEGER,
    rgdpe NUMERIC,
    rgdpo NUMERIC,
    emp NUMERIC,
    hc NUMERIC,
    cn NUMERIC,
    ck NUMERIC,
    popul NUMERIC,
    cftp NUMERIC,
    rtfpna NUMERIC,
    delta NUMERIC,
    csh_i NUMERIC,
    country_id INTEGER,
    FOREIGN KEY (country_id) REFERENCES countries(id)
);

.mode csv
.separator ";"
.import id.csv countries
.import economic.csv pennworld

UPDATE pennworld
    SET rgdpe = REPLACE(rgdpe, ',', '.'),
        rgdpo = REPLACE(rgdpo, ',', '.'),
        emp = REPLACE(emp, ',', '.'),
        hc = REPLACE(hc, ',', '.'),
        cn = REPLACE(cn, ',', '.'),
        ck = REPLACE(ck, ',', '.'),
        popul = REPLACE(popul, ',', '.'),
        cftp = REPLACE(cftp, ',', '.'),
        rtfpna = REPLACE(rtfpna, ',', '.'),
        delta = REPLACE(delta, ',', '.'),
        csh_i = REPLACE(csh_i, ',', '.');
