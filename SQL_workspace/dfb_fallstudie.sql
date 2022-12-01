-- author: Mei Xue 
-- Fallstudie „DFB“ zur Datenmodellierung
CREATE DATABASE IF NOT EXISTS dfb;

use dfb;


DROP TABLE IF EXISTS `Spieler`;
DROP TABLE IF EXISTS `Städte`;

-- Tabellen, Spalten und Beziehungen definieren
-- Jede Tabelle enthält nur Attribute eines einzigen Entitätstyps, und die Redundanz kann reduziert werden.
-- Datenqualität : Attribut-Constraints, Key-Constraints und referentielle Integrität
CREATE TABLE `Städte` (
	`stadt_id` varchar(10) NOT NULL,
	`stadt` varchar(255) NOT NULL,
	`land_id` varchar(10) NOT NULL,
	PRIMARY KEY (`stadt_id`)
);

CREATE TABLE `Spieler` (
	`Spieler_id` INT NOT NULL AUTO_INCREMENT,
	`Vorname` varchar(255) NOT NULL,
	`Nachname` varchar(255) NOT NULL,
	`Geburtsdatum` DATE NOT NULL,
	`Alter` INT NOT NULL,
	`Staatsangehörigkeit_id` varchar(10) NOT NULL,
	`Telefonnummer` varchar(20) UNIQUE,
	`Wohnort_stadt_id` varchar(10),
	`Vereinsmannschaft_id` varchar(20) NOT NULL,
    `Spieler_status` varchar(255) NOT NULL DEFAULT 'aktueller Nationalspieler',
	PRIMARY KEY (`Spieler_id`)
);

CREATE TABLE `Länder` (
	`land_id` varchar(10) NOT NULL,
	`land_name` varchar(255) NOT NULL UNIQUE,
	PRIMARY KEY (`land_id`)
);

CREATE TABLE `Bewertende_person` (
	`bp_id` INT NOT NULL AUTO_INCREMENT,
	`Vorname` varchar(255) NOT NULL,
	`Nachname` varchar(255) NOT NULL,
	PRIMARY KEY (`bp_id`)
);

CREATE TABLE `Vereinsmannschaft` (
	`Vereinsmannschaft_id` varchar(20) NOT NULL,
	`Vereinsmannschaft_name` varchar(255) NOT NULL UNIQUE,
	PRIMARY KEY (`Vereinsmannschaft_id`)
);

CREATE TABLE `Spielerbewertung` (
	`Spiel_id` INT NOT NULL,
	`Spieler_id` INT NOT NULL,
	`Bewertung` DECIMAL(5,2) NOT NULL,
	`Torschüsse` INT ,
	`Tore` INT  ,
	`Torvorlagen` INT ,
	`Gelbe_karten` INT,
	`Rote_karten` INT,
	`Ballberührungen` INT,
	`Gelaufene_distanz` INT,
	`Kapitän` BOOLEAN,
	`Bewertende_person_id` INT ,
	`Bewertung_text` TEXT,
	PRIMARY KEY (`Spiel_id`,`Spieler_id`)
);

CREATE TABLE `Länderspielen` (
	`Spiel_id` INT NOT NULL AUTO_INCREMENT,
	`Spieldatum` DATE NOT NULL,
	`Spiel_ort` varchar(10) NOT NULL,
	`Gegner` varchar(10) NOT NULL,
	`Ergebnis` BOOLEAN,
	`Spiel_typ` varchar(255) NOT NULL,
	`Zuschauerzahl` INT NOT NULL,
	`Zuschauereinnahmen` INT NOT NULL,
	`Sponsoreneinnahmen` INT NOT NULL,
	PRIMARY KEY (`Spiel_id`)
);

CREATE TABLE `Finanzzahlung` (
	`Zahlung_id` INT NOT NULL AUTO_INCREMENT,
	`Empfänger_id` INT NOT NULL,
	`Zahlungsname` varchar(255) NOT NULL,
	`Zahlungstyp` varchar(255) NOT NULL DEFAULT 'Lastschrift',
	`Zahlungsdatum` DATE NOT NULL,
	`Zahlungsbetrag` DECIMAL(20,2) NOT NULL,
	`Zahlungswährung` varchar(255) NOT NULL DEFAULT 'Euro',
	`Zahlungsabwicklung` varchar(255) NOT NULL,
	`Zahlungsstatus` BOOLEAN,
	PRIMARY KEY (`Zahlung_id`)
);

-- referentielle Integrität-Constraint ist durch einen Fremdschlüssel erzwungen.
-- ihre Domäne und ihr Datentyp müssen gleich sein, und jeder Wert im Fremdschlüssel muss im Primärschlüssel der anderen Tabelle vorhanden sein
-- Es ist auch möglich, alle betreffenden Einträge sowohl in der Kind- als auch in der Eltern-Tabelle gleichzeitig zu löschen oder zu aktualisieren. on delete/update + cascade
ALTER TABLE `Städte` ADD CONSTRAINT `Städte_fk0` FOREIGN KEY (`land_id`) REFERENCES `Länder`(`land_id`) on update cascade ;

ALTER TABLE `Spieler` ADD CONSTRAINT `Spieler_fk0` FOREIGN KEY (`Staatsangehörigkeit_id`) REFERENCES `Länder`(`land_id`);

ALTER TABLE `Spieler` ADD CONSTRAINT `Spieler_fk1` FOREIGN KEY (`Wohnort_stadt_id`) REFERENCES `Städte`(`stadt_id`);

ALTER TABLE `Spieler` ADD CONSTRAINT `Spieler_fk2` FOREIGN KEY (`Vereinsmannschaft_id`) REFERENCES `Vereinsmannschaft`(`Vereinsmannschaft_id`);

ALTER TABLE `Spielerbewertung` ADD CONSTRAINT `Spielerbewertung_fk0` FOREIGN KEY (`Spiel_id`) REFERENCES `Länderspielen`(`Spiel_id`);

ALTER TABLE `Spielerbewertung` ADD CONSTRAINT `Spielerbewertung_fk1` FOREIGN KEY (`Spieler_id`) REFERENCES `Spieler`(`Spieler_id`);

ALTER TABLE `Spielerbewertung` ADD CONSTRAINT `Spielerbewertung_fk2` FOREIGN KEY (`Bewertende_person_id`) REFERENCES `Bewertende_person`(`bp_id`);

ALTER TABLE `Länderspielen` ADD CONSTRAINT `Länderspielen_fk0` FOREIGN KEY (`Spiel_ort`) REFERENCES `Städte`(`stadt_id`);

ALTER TABLE `Länderspielen` ADD CONSTRAINT `Länderspielen_fk1` FOREIGN KEY (`Gegner`) REFERENCES `Länder`(`land_id`);

ALTER TABLE `Finanzzahlung` ADD CONSTRAINT `Finanzzahlung_fk0` FOREIGN KEY (`Empfänger_id`) REFERENCES `Spieler`(`Spieler_id`);

-- physische Datenmodell : Partitionen, CPUs, Indizes
-- Indizes für einige Tabellen erstellen, um die Suche/Abfrage zu beschleunigen.
create unique index spielerid on spieler (Spieler_id);

-- Für umfassende Spielerstatistiken: Ansichten erstellen
-- die spieler_id und die Anzahl der Länderspiele für A-Mannschaft als Ausgabe der Ansicht count_a 
create view `count_a` as 
select Spieler_id, count(*) as `Anzahl_A_Mannschaft` from spielerbewertung as s
left join `länderspielen` as l on s.Spiel_id =l.Spiel_id
where  Spiel_typ ='Länderspiel A-Mannschaft' 
group by Spieler_id;

-- die Anzahl der Länderspiele für Junioren-Nationalmannschaften 
create view count_j as
select Spieler_id, count(*) as `Anzahl_Junioren_Mannschaft` from spielerbewertung as s
left join `länderspielen` as l on s.Spiel_id =l.Spiel_id
where  Spiel_typ ='Länderspiel Junioren-Nationalmannschaften'
group by Spieler_id;

-- Durchschnittliche Bewertung der letzten 5 Spiele jedes Spielers
-- zunächst die letzten fünf Spiele für jeden Spieler ermitteln => gruppierte Top N-Analyse 
-- Analyse-Funktion row_number() over(partition by…), nach der Spieler-ID zu gruppieren, nach dem Spieldatum zu sortieren , um die gruppierte & geordnete Zeilen-Nummer anzahl_spiel zu erhalten, 
-- und setzen diese Abfrage als Tabelle a ein, dann filtern und gruppieren
create view `avg_letzten_5` as
select a.Spieler_id, avg(a.Bewertung) as `avg_bewertung_letzten_5` 
from (
	select s.Spieler_id, s.Bewertung, 
    row_number() over (partition by s.Spieler_id order by l.Spieldatum desc) as anzahl_spiel
    from spielerbewertung as s 
    left join `länderspielen` as l
    on s.Spiel_id =l.Spiel_id
) as a
where a.anzahl_spiel < 6
group by a.Spieler_id ;


-- Durchschnittliche Bewertung der Spiele der aktuellen Saison
create view `avg_akt_saison` as
select s.Spieler_id, avg(s.Bewertung) as `avg_aktuellen_Saison`
from spielerbewertung as s 
left join `länderspielen` as l
on s.Spiel_id =l.Spiel_id
where l.Spieldatum between '2022-08-01' and '2023-06-01'
group by s.Spieler_id;

-- Durchschnittliche Bewertung der Spiele insgesamt
create view `avg_insgesamt` as
select Spieler_id, avg(Bewertung) as avg_Bewertung_insgesamt
from spielerbewertung 
group by Spieler_id;

-- Durchschnittliche Bewertung der letzten 5 Länderspiele
create view `avg_letzten_5_länder` as
select a.Spieler_id, avg(a.Bewertung) as `avg_letzten_5_länderspiele` 
from (
	select s.Spieler_id, s.Bewertung, 
    row_number() over (partition by s.Spieler_id order by l.Spieldatum desc) as anzahl_spiel
    from spielerbewertung as s 
    left join `länderspielen` as l
    on s.Spiel_id =l.Spiel_id
    where l.Spiel_typ like '%Länderspiel%'
) as a
where a.anzahl_spiel < 6
group by a.Spieler_id ;

-- Durchschnittliche Bewertung der Länderspiele der aktuellen Saison
create view avg_länderspiel_akt_saison as
select s.Spieler_id, avg(s.Bewertung) as `avg_länderspiel_aktuellen_Saison`
from spielerbewertung as s 
left join `länderspielen` as l
on s.Spiel_id =l.Spiel_id
where l.Spieldatum between '2022-08-01' and '2023-06-01' 
and l.Spiel_typ like '%Länderspiel%'
group by s.Spieler_id;

-- Durchschnittliche Bewertung der Länderspiele insgesamt
create view `avg_Länderspiel_insg` as
select Spieler_id, avg(Bewertung) as `avg_länderspiel_insgesamt`
from spielerbewertung
where Spiel_id in ( 
	select Spiel_id from `länderspielen` 
    where Spiel_typ like '%Länderspiel%')
group by Spieler_id;

-- Prämienzahlung der aktuellen Saison
create view zahlung_akt_saison as
select Empfänger_id, sum(Zahlungsbetrag) as prämie_aktuellen_saison
from finanzzahlung 
where Zahlungsdatum between '2022-08-01' and '2023-06-01'
group by Empfänger_id;

-- Prämienzahlung während der Nationalmannschaftskarriere
create view zahlung_karriere as
select Empfänger_id, sum(Zahlungsbetrag) as Prämie_karriere
from finanzzahlung 
group by Empfänger_id;

-- Aktuell ausstehende Prämienzahlungen
-- die Einträge auf den Zahlungsstatus false filtert und nach Empfänger_id gruppiert
create view ausstehende_zahlung as
select Empfänger_id, sum(Zahlungsbetrag) as ausstehende_Prämienzahlung
from finanzzahlung 
where Zahlungsstatus = false
group by Empfänger_id;

-- die spieler-Tabelle und diese Ansichten mit Hilfe Left-Join kombiniert, 
-- um die Ansicht umfassende_statistik zu bilden.
-- die Ansicht immer die neuesten Daten anzeigen
create view umfassende_statistik as
select s.Spieler_id, s.Vorname, s.Nachname, a.Anzahl_A_Mannschaft, b.Anzahl_Junioren_Mannschaft,
 c.avg_bewertung_letzten_5, d.avg_aktuellen_Saison, e.avg_Bewertung_insgesamt,
 f.avg_letzten_5_länderspiele, g.avg_länderspiel_aktuellen_Saison,
 h.avg_länderspiel_insgesamt, i.prämie_aktuellen_saison, j.Prämie_karriere,
 k.ausstehende_Prämienzahlung
from spieler as s 
left join count_a as a on s.Spieler_id = a.Spieler_id
left join count_j as b on s.Spieler_id = b.Spieler_id 
left join avg_letzten_5 as c on s.Spieler_id = c.Spieler_id
left join avg_akt_saison as d on s.Spieler_id = d.Spieler_id 
left join avg_insgesamt as e on s.Spieler_id = e.Spieler_id 
left join avg_letzten_5_länder as f on s.Spieler_id =f.Spieler_id
left join avg_länderspiel_akt_saison as g on s.Spieler_id =g.Spieler_id
left join avg_länderspiel_insg as h on s.Spieler_id = h.Spieler_id
left join zahlung_akt_saison as i on s.Spieler_id = i.Empfänger_id
left join zahlung_karriere as j on s.Spieler_id = j.Empfänger_id
left join ausstehende_zahlung as k on s.Spieler_id =k.Empfänger_id;

select * from umfassende_statistik;

-- Insert Statement für das Einfügen der ersten Datensätze in diese Tabellen
-- gemäß der Integritätsbeschränkung
insert into länder
values ('DE', 'Deutschland');

insert into städte
values 
('M', 'München', 'DE'),
('WOR','Wolfratshausen','DE');

insert into vereinsmannschaft
values ('FC Bayern', 'Fußball-Club Bayern, München e. V.');

INSERT INTO spieler
VALUES 
(1, 'Manuel', 'Neuer', '1986-03-27', 0, 'DE', '017686095114', 'M', 'FC Bayern', 'aktueller Nationalspieler'),
(2, 'Gerhard','Müller','1945-11-03', 0, 'DE', '016732517255', 'WOR','FC Bayern', 'Karriereende' );

-- Das Alter der Spieler wird automatisch mit der UPDATE-Statement aktualisiert. 
update spieler as s 
set s.Alter = timestampdiff(year, Geburtsdatum, curdate());


insert into länderspielen 
values
(1, '1965-08-01', 'M', 'DE', 1, 'Länderspiel A-Mannschaft', 200000, 500000, 10000000),
(11, '1971-09-01', 'M', 'DE', 1, 'Länderspiel A-Mannschaft', 200000, 500000, 10000000),
(23, '1969-08-01', 'M', 'DE', 1, 'Länderspiel A-Mannschaft', 200000, 500000, 10000000),
(67, '1980-08-01', 'M', 'DE', 1, 'Länderspiel A-Mannschaft', 200000, 500000, 10000000);

insert into spielerbewertung(Spiel_id, Spieler_id, Bewertung)
values 
(1 , 2, 2.0),
(11, 2, 1.5),
(23, 2, 1.8);

-- Idealtypische Abfrage aller aktuellen Nationalspieler
-- zwei Tabellen mit join verbunden werden & die Einträge mit where-Anweisung gefiltert werden. 
select u.* from umfassende_statistik as u
left join spieler as s
on u.Spieler_id = s.Spieler_id
where s.Spieler_status = 'aktueller Nationalspieler';

-- Idealtypische Abfrage aller aktuellen Nationalspieler
-- die Einträge mit where-Anweisung gefiltert werden
select * from umfassende_statistik
where Spieler_id in (select Spieler_id from spieler 
					where Spieler_status = 'aktueller Nationalspieler');
                    
                    
-- Idealtypische Abfrage der letzten 3 Spiele bzw. Spielbewertungen zu Spieler Gerd Müller
-- die Tabelle zu verbinden, row_number() nach spieler_id zu gruppieren, nach dem Spieldatum zu sortieren, 
-- nach den Namen zu filtern,  und die Top 3 Einträge mit anzahl_spiel<4 oder limit 3 auszugeben. 
-- Stored Procedure, der Name des Spielers als Parameter => letzten 3 Spielbewertungen eines beliebigen Spielers abfragen
DELIMITER //
create procedure bewertung_spieler(in Vorname varchar(255), in Nachname varchar(255) )
begin
select a.Spieler_id, b.Vorname, b.Nachname, a.Bewertung  
from (
	select s.Spieler_id, s.Bewertung, 
    row_number() over (partition by s.Spieler_id order by l.Spieldatum desc) as anzahl_spiel
    from `spielerbewertung` as s 
    left join `länderspielen` as l
    on s.Spiel_id =l.Spiel_id
) as a
left join `spieler` as b on a.Spieler_id = b.Spieler_id
where b.Vorname =Vorname  and b.Nachname= Nachname
-- and a.anzahl_spiel < 4 ;
limit 3 ;
end //
DELIMITER ; 

call bewertung_spieler('Gerhard','Müller');

-- Idealtypische Abfrage der aktuell offenen Prämienzahlungen an die Nationalspieler
-- die Tabelle spieler und die Ansicht ausstehende_zahlung(Zeile 215) zu verknüpfen. 
select s.Spieler_id, s.Vorname, s.Nachname, a.ausstehende_Prämienzahlung 
from spieler as s 
left join ausstehende_zahlung as a
on s.Spieler_id =a.Empfänger_id;



