INSERT INTO agency (
  iata_id,
  agency,
  city,
  country
)
VALUES 
  ('NYC', 'Metropolitan Transportation Authority (MTA)', 'New York', 'United States'),
  ('BOS', 'Massachusetts Bay Transportation Authority (MBTA)', 'Boston', 'United States'),
  ('PHL', 'Southeastern Pennsylvania Transportation Authority (SEPTA)', 'Philadelphia', 'United States'),
  ('PIT', 'Pittsburgh Regional Transit (PRT)', 'Pittsburgh', 'United States'),
  ('SFO', 'Bay Area Rapid Transit (BART)', 'San Francisco', 'United States')
ON CONFLICT DO NOTHING;
