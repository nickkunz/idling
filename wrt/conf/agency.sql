WITH j (iata_id, agency, city, country) AS (
  VALUES 
    ('NYC', 'Metropolitan Transportation Authority (MTA)', 'New York', 'United States'),
    ('BOS', 'Massachusetts Bay Transportation Authority (MBTA)', 'Boston', 'United States'),
    ('PHL', 'Southeastern Pennsylvania Transportation Authority (SEPTA)', 'Philadelphia', 'United States'),
    ('PIT', 'Pittsburgh Regional Transit (PRT)', 'Pittsburgh', 'United States'),
    ('SFO', 'Bay Area Rapid Transit (BART)', 'San Francisco', 'United States')
)
INSERT INTO agency (iata_id, agency, city, country)
SELECT i.iata_id, i.agency, i.city, i.country
FROM j i
LEFT JOIN agency k ON k.iata_id = i.iata_id
WHERE k.iata_id IS NULL;
