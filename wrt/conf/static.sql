SELECT * FROM events
JOIN agency ON events . iata_id = agency . iata_id
WHERE events . datetime
BETWEEN EXTRACT ( EPOCH FROM TIMESTAMP ’2023 -11 -01’)
AND EXTRACT ( EPOCH FROM TIMESTAMP ’2023 -12 -01’);