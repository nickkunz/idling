CREATE TABLE IF NOT EXISTS agency (
    iata_id VARCHAR(255),
    agency VARCHAR(255),
    city VARCHAR(255),
    country VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS events (
    iata_id VARCHAR(255),
    vehicle_id VARCHAR(255),
    trip_id VARCHAR(255),
    route_id VARCHAR(255),
    latitude FLOAT,
    longitude FLOAT,
    datetime INT,
    duration INT,
    CONSTRAINT unique_columns UNIQUE (
        vehicle_id,
        trip_id,
        route_id,
        latitude,
        longitude
    )
);
