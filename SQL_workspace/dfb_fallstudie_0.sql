CREATE TABLE `Städte` (
	`stadt_id` varchar(10) NOT NULL,
	`stadt` varchar(255) NOT NULL,
	`PLZ` varchar(10) NOT NULL UNIQUE,
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
	`Torschüsse` INT NOT NULL,
	`Tore` INT NOT NULL,
	`Torvorlagen` INT NOT NULL,
	`Gelbe_karten` INT,
	`Rote_karten` INT,
	`Ballberührungen` INT,
	`Gelaufene_distanz` INT,
	`Kapitän` BOOLEAN,
	`Bewertende_person_id` INT NOT NULL,
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

ALTER TABLE `Städte` ADD CONSTRAINT `Städte_fk0` FOREIGN KEY (`land_id`) REFERENCES `Länder`(`land_id`);

ALTER TABLE `Spieler` ADD CONSTRAINT `Spieler_fk0` FOREIGN KEY (`Staatsangehörigkeit_id`) REFERENCES `Länder`(`land_id`);

ALTER TABLE `Spieler` ADD CONSTRAINT `Spieler_fk1` FOREIGN KEY (`Wohnort_stadt_id`) REFERENCES `Städte`(`stadt_id`);

ALTER TABLE `Spieler` ADD CONSTRAINT `Spieler_fk2` FOREIGN KEY (`Vereinsmannschaft_id`) REFERENCES `Vereinsmannschaft`(`Vereinsmannschaft_id`);

ALTER TABLE `Spielerbewertung` ADD CONSTRAINT `Spielerbewertung_fk0` FOREIGN KEY (`Spiel_id`) REFERENCES `Länderspielen`(`Spiel_id`);

ALTER TABLE `Spielerbewertung` ADD CONSTRAINT `Spielerbewertung_fk1` FOREIGN KEY (`Spieler_id`) REFERENCES `Spieler`(`Spieler_id`);

ALTER TABLE `Spielerbewertung` ADD CONSTRAINT `Spielerbewertung_fk2` FOREIGN KEY (`Bewertende_person_id`) REFERENCES `Bewertende_person`(`bp_id`);

ALTER TABLE `Länderspielen` ADD CONSTRAINT `Länderspielen_fk0` FOREIGN KEY (`Spiel_ort`) REFERENCES `Städte`(`stadt_id`);

ALTER TABLE `Länderspielen` ADD CONSTRAINT `Länderspielen_fk1` FOREIGN KEY (`Gegner`) REFERENCES `Länder`(`land_id`);

ALTER TABLE `Finanzzahlung` ADD CONSTRAINT `Finanzzahlung_fk0` FOREIGN KEY (`Empfänger_id`) REFERENCES `Spieler`(`Spieler_id`);









