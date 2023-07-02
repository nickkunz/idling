WITH j AS (
    SELECT * FROM idle
    WHERE vehicle_id = %s
    AND trip_id = %s
    AND route_id = %s
    AND latitude = %s
    AND longitude = %s
    ORDER BY duration DESC
    LIMIT 1
)
INSERT INTO idle (
    vehicle_id,
    trip_id,
    route_id,
    latitude,
    longitude,
    datetime,
    duration,
    source
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
WHERE idle.duration < EXCLUDED.duration;