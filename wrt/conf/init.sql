CREATE TABLE IF NOT EXISTS idle (
    id SERIAL PRIMARY KEY,
    vehicle_id TEXT,
    trip_id TEXT,
    route_id TEXT,
    latitude FLOAT,
    longitude FLOAT,
    datetime INT,
    duration INT,
    source TEXT,
    CONSTRAINT unique_columns UNIQUE (
        vehicle_id,
        trip_id,
        route_id,
        latitude,
        longitude
    )
);
