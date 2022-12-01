use market;

set SQL_SAFE_UPDATES = 0;
delete from startups_in_deutschland  where Unternehmensname is null;
