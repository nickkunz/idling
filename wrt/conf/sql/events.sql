WITH j AS (
    SELECT * FROM events
    WHERE iata_id = %s
    AND vehicle_id = %s
    AND trip_id = %s
    AND route_id = %s
    AND latitude = %s
    AND longitude = %s
    ORDER BY duration DESC
    LIMIT 1
    FOR UPDATE
)
INSERT INTO events (
    iata_id,
    vehicle_id,
    trip_id,
    route_id,
    latitude,
    longitude,
    datetime,
    duration
)
SELECT %s, %s, %s, %s, %s, %s, %s, %s
WHERE NOT EXISTS (
    SELECT 1
    FROM j
)
OR %s > COALESCE((SELECT duration FROM j), 0)
ON CONFLICT (
    vehicle_id,
    trip_id,
    route_id,
    latitude,
    longitude
)
DO UPDATE SET duration = EXCLUDED.duration
WHERE events.duration < EXCLUDED.duration;
