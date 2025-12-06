PRAGMA foreign_keys = ON;

CREATE TABLE umiejetnosc (
  id_umiejetnosc INTEGER PRIMARY KEY AUTOINCREMENT,
  nazwa varchar(20) NOT NULL UNIQUE,
  opis TEXT
);

CREATE TABLE klimaty(
  id_klimat INTEGER PRIMARY KEY AUTOINCREMENT,
  typ VARCHAR(20) NOT NULL UNIQUE,
  srednia_temperatura decimal(5,2) CHECK (srednia_temperatura BETWEEN -100 and 200)
);

CREATE TABLE planety(
  id_planeta INTEGER PRIMARY KEY AUTOINCREMENT,
  id_klimat int,
  nazwa VARCHAR(20) NOT NULL UNIQUE, 
  srednica_km int CHECK (srednica_km > 0),
  Populacja BIGINT,
  opis TEXT,
  FOREIGN KEY (id_klimat) REFERENCES klimaty(id_klimat)
);

CREATE TABLE organizacja( 
  id_organizacja INTEGER PRIMARY KEY AUTOINCREMENT,
  nazwa varchar(20) NOT NULL UNIQUE,
  typ varchar(50),
  data_zalozenia DATE,
  opis text
);

CREATE TABLE postacie (
  id_postac INTEGER PRIMARY KEY AUTOINCREMENT,
  id_organizacja INT,
  imie varchar(20),
  nazwisko varchar(20),
  data_urodzenia DATE,
  data_smierci DATE NULL,
  czy_zyje INTEGER,
  plec VARChar(10) CHECK (plec in ('M','K','Nieznana')),
  opis TEXT,
  FOREIGN KEY (id_organizacja) REFERENCES organizacja(id_organizacja)
);

CREATE TABLE postacie_umiejetnosci ( 
  id_postac INT,
  id_umiejetnosc INT,
  poziom int CHECK (poziom BETWEEN 1 and 10),
  FOREIGN KEY (id_postac) REFERENCES postacie(id_postac),
  FOREIGN KEY (id_umiejetnosc) REFERENCES umiejetnosc(id_umiejetnosc)
);

CREATE TABLE technologie(
  id_technologia INTEGER PRIMARY KEY AUTOINCREMENT,
  id_organizacja int,
  nazwa varchar (20) NOT NULL UNIQUE,
  poziom_zaawansowania INT CHECK (Poziom_zaawansowania BETWEEN 1 AND 10),
  opis text,
  FOREIGN KEY (id_organizacja) REFERENCES organizacja(id_organizacja)
);

CREATE TABLE wydarzenia(
  id_wydarzenie INTEGER PRIMARY KEY AUTOINCREMENT,
  id_planeta int,
  Nazwa Varchar(100) NOT NULL UNIQUE,
  Data DATE,
  Opis TEXT,
  FOREIGN KEY (id_planeta) REFERENCES planety(id_planeta)
);

CREATE TABLE wydarzenia_postacie(
  id_wydarzenie INT,
  id_postac int,
  rola VARCHAR(200),
  FOREIGN KEY (id_wydarzenie) REFERENCES wydarzenia(id_wydarzenie),
  FOREIGN KEY (id_postac) REFERENCES postacie(id_postac)
);

CREATE TABLE zasoby(
  id_zasob INTEGER PRIMARY KEY AUTOINCREMENT,
  nazwa varchar(20) NOT NULL UNIQUE,
  Rzadkosc INT CHECK (Rzadkosc BETWEEN 1 AND 10),
  Wartosc_za_jednostke DECIMAL(10,2)
);

CREATE TABLE planety_zasoby(
  id_planeta int,
  id_zasob int,
  ilosc dec(12,2),
  FOREIGN KEY (id_planeta) REFERENCES planety(id_planeta),
  FOREIGN KEY (id_zasob) REFERENCES zasoby(id_zasob)
);

CREATE TABLE organizacje_planety(
  id_organizacja int,
  id_planeta int,
  typ_kontroli Varchar(20) CHECK (typ_kontroli IN ('Siedziba','Kolonizacja','Okupacja')),
  FOREIGN KEY (id_planeta) REFERENCES planety(id_planeta),
  FOREIGN KEY (id_organizacja) REFERENCES organizacja(id_organizacja)
);

INSERT INTO klimaty (typ, srednia_temperatura) 
VALUES 
('Pustynny', 45.5),
('Umiarkowany', 25.4),
('Wulkaniczny', 66.6),
('Lodowy', -60),
('Tropikalny', 30.5);

INSERT INTO zasoby ( nazwa, rzadkosc, wartosc_za_jednostke)
VALUES 
('Melanż', 10, 1000000.00),
('Woda',6, 10000.00),
('Ropa Lazurowa', 3, 5000.00),
('Holtzmanit', 8, 150000.00),
('złoto',2, 2000.00);

INSERT INTO umiejetnosc( nazwa, opis)
VALUES
('Przetrwanie', 'umniejętnośc przeżycia w ekstremalnych warunkach'),
('Presja głosu', 'moc która pozwala Bene Gesserit kontrolować ludzi głosem'),
('Nawigacja', 'umiejętnośc nawgiowania statkiem kosmiczny po galaktyce'),
('Walka bronią biała', 'umiejętność posługiwania sie bronią biała w walce'),
('Przewidywanie', 'Postacie dzięki treningowi i zażywaniu melanżu są w stanie przewidywać przyszłość w różnym zakresie');

INSERT INTO planety(nazwa, srednica_km, populacja, opis, id_klimat)
VALUES 
('Arrakis', 10190, 13000000, 'Pustyny świat zamieszkany przez Fremenów, jedyne miejsce z zasobami melanżu', 1),
('Caladan', 12500, 3000000000, 'Wodnista Planeta, siedziba rodu Atrydów', 2),
('Kaitan', 14000, 17500000000, 'Stolica Imperium', 2),
('Giedi Prime', 11000, 10000000000, 'Industrialna planeta siedziba rodu harkonen', 2),
('Salusa Secundus', 95000, 150000000, 'Surowa planeta używana jako kolonia karna do szkolenia elitarnych wojowników',3);

INSERT INTO organizacja( nazwa, typ , data_zalozenia, opis)
VALUES
('Atrydzi','Ród', '1234-07-01','Szlachetny ród z Caladanuu' ),
('Bene Geserit', 'Sekta', '0201-01-01','Tajny żeński zakon o ogr...ym i genetycznym w imperium Diuny, działający od tysięcy lat' ),
('Harkoneni', 'Ród', '1156-11-23','Ród Harkonnenów to jeden z Wi...ny z brutalności, korupcji i bezwzględnego dążenia do władzy.'),
('Gildia kosmiczna', 'Gildia', '0456-03-15', 'organizacja opdowiedzialana za podróże kosmiczne' ),
('Fremeni', 'Plemie', '0567-05-30','Rdzenny Lud Arrakis przystosowany do życia na surowej pustynej planecie');

INSERT INTO planety_zasoby(id_planeta, id_zasob, ilosc)
VALUES
(1, 1, 10000),
(1, 2, 50),
(2, 2, 1000000),
(4, 3, 5030000),
(3, 5, 3450);

INSERT INTO organizacje_planety(id_organizacja, id_planeta, typ_kontroli)
VALUES 
(1, 1, 'Kolonizacja'),
(1, 2, 'Siedziba'),
(3, 4, 'Siedziba'),
(5, 1, 'Siedziba');

INSERT INTO technologie(nazwa, poziom_zaawansowania, opis, id_organizacja)
VALUES
('Nawigacja Kosmiczna', 10, 'Pozwala na bezpieczną i szybką podróż koszmiczną', 4),
('Tarcza Holtzmana', 10, 'Ochrania przed szybkimi pociskami', 4),
('Destylatory Fremenów', 6, 'Pozwala zbierać wilgoć z powietrza', 5),
('Ornitoptery',8, 'Heliktopodobny pojazd latający', 1),
('Przepowiednie krwi',9, 'Genetyczne przepowiednie przyszłości',2);

INSERT INTO postacie(imie, nazwisko, data_urodzenia, data_smierci, czy_zyje, plec, opis, id_organizacja)
VALUES
('Paul', 'Atryda', '1175-03-15', '1205-09-01', 0, 'M','Książę Caladanu',1),
('Leto II','Atryda','1200-05-23','2340-10-02', 0, 'M','Kwizatz Haderach',1),
('Vladimir', 'Harkonnen', '1120-11-30', '1175-10-01', 0, 'M', 'Baron Harkonnen',3),
('Stilgar', 'Fremen', '1100-05-25', NULL, 1, 'M',  'Naczelnik Fremenów', 5),
('Gaius Helen ','Mohiam','1090-11-23','1200-10-12',0,'K','Wielebna Matka Bene Gesserit',2);

INSERT INTO postacie_umiejetnosci(id_postac, id_umiejetnosc,poziom)
VALUES
(1,1,9),
(1,2,7),  
(1,4,8),
(1,5,8),
(2,1,10),
(2,2,10),
(2,5,10),
(3,1,2),
(4,1,10),
(4,4,9),
(5,2,9),
(5,5,6);

INSERT INTO wydarzenia(nazwa, data, Opis, id_planeta)
VALUES
('Bitwa o arrakis', '1075-10-12', 'Ostateczna bitwa o władze nad arrakis',1),
('Zjazd Landsraadu', '1170-05-15', 'Spotkanie wielkich rodów',3),
('Igrzyska na Giedi Prime', '0175-08-10', 'Widowiskowe rozprawianie sie z resztą rodu Atrydów',4),
('Przemiana Leto II','1240-10-24', 'Fuzja Leto II i wielkiego czerwia',1),
('Próba Paula', '1074-04-23', 'Próba Bene Geserit na Paulu', 2);

INSERT INTO wydarzenia_postacie(id_wydarzenie, id_postac, Rola)
VALUES
(1,1,'Przywódca'),
(1,4,'Generał'),
(2,3,'Reprezentant'),
(3,2,'Obserwator'),
(4,2,'Przemieniony'),
(5,1,'Testowany'),
(5,5,'Testująca');
