CREATE TABLE IF NOT EXISTS agency (
    iata_id VARCHAR(255) PRIMARY KEY,
    agency VARCHAR(255) UNIQUE,
    city VARCHAR(255) UNIQUE,
    country VARCHAR(255),
    region VARCHAR(255),
    continent VARCHAR(255)
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
