WITH RECURSIVE date_range AS (
  SELECT
    DATE_TRUNC('day', MIN(TO_TIMESTAMP(datetime))) AS start_date,
    DATE_TRUNC('day', MAX(TO_TIMESTAMP(datetime))) + INTERVAL '1 day' AS end_date
  FROM events
  UNION ALL
  SELECT
    start_date - INTERVAL '1 day',
    end_date - INTERVAL '1 day'
  FROM date_range
  WHERE start_date > (SELECT DATE_TRUNC('day', MIN(TO_TIMESTAMP(datetime))) FROM events)
), cte AS (
  SELECT
    agency.*,
    events.vehicle_id,
    events.trip_id,
    events.latitude,
    events.datetime,
    events.route_id,
    events.longitude,
    events.duration,
    DATE_TRUNC('day', TO_TIMESTAMP(events.datetime)) AS day
  FROM agency
  INNER JOIN events ON agency.iata_id = events.iata_id
)
SELECT
  *
FROM (
  SELECT
    cte.*,
    LAG(datetime, 1) OVER (PARTITION BY day ORDER BY datetime) AS prev_datetime
  FROM cte
  INNER JOIN date_range ON cte.day BETWEEN date_range.start_date AND date_range.end_date - INTERVAL '1 day'
) t
WHERE (prev_datetime IS NULL AND datetime IS NOT NULL)
   OR (prev_datetime IS NOT NULL AND datetime - prev_datetime <= 600)
ORDER BY day, datetime;