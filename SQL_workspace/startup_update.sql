SELECT * FROM market.startups_in_deutschland;
update startups_in_deutschland_n2 as s inner join masterliste as m
on m.Firmenname = s.Unternehmensname 
set 
s.`Gruender:in aktuell in leitender Position` = m.`Bezug zur FSU`, 
s.`(Gruender:innen-) Hochschule` =m.`(Gruender-)Hochschule`,
s.`Informationen (Deutschland): Anschrift - stra?e, hausnummer`=m.`Strasse`,
s.`Informationen (Deutschland): Anschrift - plz`=m.`PLZ`,
s.`Informationen (Deutschland): Anschrift - region`=m.`Ort`,
s.`akt. Beteiligung der Gruender:innen` =m.`Beteiligung der Gruender`,
s.`Gesellschafter:innen` =m.`Gesellschafter`;

select Unternehmensname , `Informationen (Deutschland): Anschrift - stra?e, hausnummer` from startups_in_deutschland;

select  count(Unternehmensname), `Informationen: Land`,
`Informationen (Deutschland): Anschrift - stra?e, hausnummer` from startups_in_deutschland;