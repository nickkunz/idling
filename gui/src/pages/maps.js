// libraries
import React, { useState, useEffect, useCallback, useContext } from 'react';
import DeckGL from '@deck.gl/react';
import { Map } from 'react-map-gl';
import { ColumnLayer, ScatterplotLayer } from '@deck.gl/layers';
import { v } from '../styles/variables';
import { ThemeContext } from '../App';
import RangeInput from '../components/slider/Slider';

// params
const REACT_APP_MAPBOX_TOKEN = process.env.REACT_APP_MAPBOX_TOKEN;
const MAP_ZOOM = 12;

const cityData = [
    { name: 'New York', iata_id: 'NYC', coordinates: { longitude: -74.0060, latitude: 40.7128 } },
    { name: 'Philadelphia', iata_id: 'PHL', coordinates: { longitude: -75.1652, latitude: 39.9526 } },
    { name: 'Washington D.C.', iata_id: 'DCA', coordinates: { longitude: -77.0369, latitude: 38.9072 } },
    { name: 'Boston', iata_id: 'BOS', coordinates: { longitude: -71.0589, latitude: 42.3601 } },
    { name: 'Pittsburgh', iata_id: 'PIT', coordinates: { longitude: -79.9959, latitude: 40.4406 } },
    { name: 'Los Angeles', iata_id: 'LAX', coordinates: { longitude: -118.2437, latitude: 34.0522 } },
    { name: 'San Francisco', iata_id: 'SFO', coordinates: { longitude: -122.41669, latitude: 37.7853 } },
    { name: 'San Diego', iata_id: 'SAN', coordinates: { longitude: -117.161087, latitude: 32.715736 } },
    { name: 'Seattle', iata_id: 'SEA', coordinates: { longitude: -122.3321, latitude: 47.6062 } },
    { name: 'Sacramento', iata_id: 'SMF', coordinates: { longitude: -121.4944, latitude: 38.5816 } },
    { name: 'Portland', iata_id: 'PDX', coordinates: { longitude: -122.6784, latitude: 45.5152 } },
    { name: 'Atlanta', iata_id: 'ATL', coordinates: { longitude: -84.3880, latitude: 33.7490 } },
    { name: 'Miami', iata_id: 'MIA', coordinates: { longitude: -80.1918, latitude: 25.7617 } },
    { name: 'Tampa', iata_id: 'TPA', coordinates: { longitude: -82.4572, latitude: 27.9506 } },
    { name: 'Louisville', iata_id: 'SDF', coordinates: { longitude: -85.7585, latitude: 38.2527 } },
    { name: 'Nashville', iata_id: 'BNA', coordinates: { longitude: -86.7816, latitude: 36.1627 } },
    { name: 'Minneapolis', iata_id: 'MSP', coordinates: { longitude: -93.2650, latitude: 44.9778 } },
    { name: 'St. Louis', iata_id: 'STL', coordinates: { longitude: -90.1994, latitude: 38.6270 } },
    { name: 'Madison', iata_id: 'MSN', coordinates: { longitude: -89.4012, latitude: 43.0731 } },
    { name: 'Columbus', iata_id: 'CMH', coordinates: { longitude: -82.9988, latitude: 39.9612 } },
    { name: 'Des Moines', iata_id: 'DSM', coordinates: { longitude: -93.6250, latitude: 41.5868 } },
    { name: 'Denver', iata_id: 'DEN', coordinates: { longitude: -104.9903, latitude: 39.7392 } },
    { name: 'Phoenix', iata_id: 'PHX', coordinates: { longitude: -112.0740, latitude: 33.4484 } },
    { name: 'San Antonio', iata_id: 'SAT', coordinates: { longitude: -98.4936, latitude: 29.4241 } },
    { name: 'Billings', iata_id: 'BIL', coordinates: { longitude: -108.5007, latitude: 45.7833 } },
    { name: 'Austin', iata_id: 'AUS', coordinates: { longitude: -97.7431, latitude: 30.2672 } },
    { name: 'Montreal', iata_id: 'YUL', coordinates: { longitude: -73.5673, latitude: 45.5017 } },
    { name: 'York', iata_id: 'YYZ', coordinates: { longitude: -79.3832, latitude: 43.6532 } },
    { name: 'Hamilton', iata_id: 'YHM', coordinates: { longitude: -79.8711, latitude: 43.2557 } },
    { name: 'Halifax', iata_id: 'YHZ', coordinates: { longitude: -63.5752, latitude: 44.6488 } },
    { name: 'Thunder Bay', iata_id: 'YQT', coordinates: { longitude: -89.2477, latitude: 48.3809 } },
    { name: 'Vancouver', iata_id: 'YVR', coordinates: { longitude: -123.1216, latitude: 49.2827 } },
    { name: 'Calgary', iata_id: 'YYC', coordinates: { longitude: -114.0719, latitude: 51.0447 } },
    { name: 'Edmonton', iata_id: 'YEG', coordinates: { longitude: -113.4909, latitude: 53.5461 } },
    { name: 'Saskatoon', iata_id: 'YXE', coordinates: { longitude: -106.6700, latitude: 52.1579 } },
    // { name: 'Victoria', iata_id: 'YYJ', coordinates: { longitude: -123.3656, latitude: 48.4284 } },
    { name: 'Amsterdam', iata_id: 'AMS', coordinates: { longitude: 4.8952, latitude: 52.3676 } },
    { name: 'Stockholm', iata_id: 'ARN', coordinates: { longitude: 18.0686, latitude: 59.3293 } },
    { name: 'Helsinki', iata_id: 'HEL', coordinates: { longitude: 24.9384, latitude: 60.1699 } },
    { name: 'Dublin', iata_id: 'DUB', coordinates: { longitude: -6.2603, latitude: 53.3498 } },
    { name: 'Rome', iata_id: 'FCO', coordinates: { longitude: 12.4964, latitude: 41.9028 } },
    { name: 'Warsaw', iata_id: 'WAW', coordinates: { longitude: 21.0122, latitude: 52.2297 } },
    { name: 'Kraków', iata_id: 'KRK', coordinates: { longitude: 19.9350, latitude: 50.0647 } },
    { name: 'Gdańsk', iata_id: 'GDN', coordinates: { longitude: 18.6466, latitude: 54.3520 } },
    { name: 'Prague', iata_id: 'PRG', coordinates: { longitude: 14.4378, latitude: 50.0755 } },
    { name: 'Sydney', iata_id: 'SYD', coordinates: { longitude: 151.2093, latitude: -33.8688 } },
    { name: 'Brisbane', iata_id: 'BNE', coordinates: { longitude: 153.0251, latitude: -27.4698 } },
    { name: 'Adelaide', iata_id: 'ADL', coordinates: { longitude: 138.6007, latitude: -34.9285 } },
    { name: 'Auckland', iata_id: 'AKL', coordinates: { longitude: 174.7633, latitude: -36.8485 } },
    { name: 'Christchurch', iata_id: 'CHC', coordinates: { longitude: 172.6362, latitude: -43.5321 } },
    { name: 'Delhi', iata_id: 'DEL', coordinates: { longitude: 77.1025, latitude: 28.7041 } }
];

// idling duration color map
function rgbMap(duration, maxDuration) {
    const intensity = duration / maxDuration;
    const greenComponent = 255 * (1 - intensity) * 0.67;  // reduce green
    return [255, greenComponent, 0];
}

// main app
function App({selectedCity  }) {
    const [data, setData] = useState([]);
    const [dataLoaded, setDataLoaded] = useState(false);
    const [currentTime, setCurrentTime] = useState(null);
    const [animationStartTime, setAnimationStartTime] = useState(null);
    const [animationEndTime, setAnimationEndTime] = useState(null);
    const [userInteracted, setUserInteracted] = useState(false);
    const [tooltipInfo, setTooltipInfo] = useState(null);
    const [isPlaying, setIsPlaying] = useState(true);
    const [tooltip, setTooltip] = useState(null);
    const [viewport, setViewport] = useState({
        longitude: 10,
        latitude: 25,
        zoom: 1.1,
        bearing: 0,
        pitch: 0
    });

    // map and sidebar style
    const { theme } = useContext(ThemeContext);
    const mapStyle = theme === 'dark' ? 'mapbox://styles/mapbox/dark-v9' : 'mapbox://styles/mapbox/light-v9';
    const maxDuration = Math.max(...data.map(d => d.properties.duration));

    // map rotation animation logic
    const animate = useCallback(() => {
        if (!userInteracted && selectedCity) {  // only animate if a city is selected
            setViewport(v => ({
                ...v,
                bearing: v.bearing + 0.1
            }));
        }
    }, [userInteracted, selectedCity]);

    useEffect(() => {
        const interval = setInterval(animate, 200);  // update every x milliseconds
        return () => clearInterval(interval);
    }, [animate]);

    // fetch data from server
    const fetchData = (url) => {
        fetch(url)
            .then(response => response.json())
            .then(fetchedData => {
                if (fetchedData.features) {
                    const timestamps = fetchedData.features.map(d =>
                        new Date(d.properties.datetime).getTime()
                    );
                    setData(fetchedData.features.map(d => ({
                        ...d,
                        timestamp: new Date(d.properties.datetime).getTime()
                    })));
                    const minTime = Math.min(...timestamps);
                    const maxTime = Math.max(...timestamps);
                    setAnimationStartTime(minTime);
                    setAnimationEndTime(maxTime);
                    setCurrentTime(minTime);
                } else {
                    console.error('Data format unexpected:', fetchedData);
                }
                setDataLoaded(true);
                setIsPlaying(true); // start the animation after data is loaded
            })
            .catch(error => console.error('Error fetching data:', error));
    };

    // posix timestamp last 24 hours
    const fetchData24Hours = () => {
        const now = new Date();
        const twentyFourHours = new Date(now.getTime() - 24 * 60 * 60 * 1000);  // last 24 hours
        return Math.floor(twentyFourHours.getTime() / 1000);  // convert to posix timestamp
    }

    // fetch data for selected city last 24 hours
    useEffect(() => {
        if (selectedCity) {
            const roundedNow = fetchData24Hours();
            fetchData(`/idle?iata_id=${selectedCity.iataId}&start_datetime=${roundedNow}`); 
        } 
    }, [selectedCity])

    // animation logic
    useEffect(() => {
        let interval;
        if (isPlaying && currentTime !== null) {
            interval = setInterval(() => {
                setCurrentTime(time => {
                    const newTime = time + 1000;  // increment every second
                    if (newTime > animationEndTime) {
                        return animationStartTime;  // reset for infinite loop
                    }
                    return newTime;
                });
            }, 200);  // update every x milliseconds
        }
        return () => clearInterval(interval);
    }, [isPlaying, currentTime, animationStartTime, animationEndTime]);

    // update view and start animation
    useEffect(() => {
        if (selectedCity) {
            setViewport(prev => ({
            ...prev,
            longitude: selectedCity.coordinates.longitude,
            latitude: selectedCity.coordinates.latitude,
            zoom: MAP_ZOOM,  // reset zoom to default
            bearing: 60,  // set bearing for the selected city
            pitch: 55  // set pitch for the selected city
            }));

            setCurrentTime(animationStartTime);
            setUserInteracted(false);
            setIsPlaying(true);  // start the animation
        }
    }, [selectedCity, animationStartTime]);

    // spacebar play/pause keyboard shortcut
    useEffect(() => {
        const handleKeyDown = (event) => {
            if (event.code === 'Space') {  // check if the key pressed is the space bar
                setIsPlaying(prevIsPlaying => !prevIsPlaying);
            }
        };
    
        window.addEventListener('keydown', handleKeyDown);
        return () => {
            window.removeEventListener('keydown', handleKeyDown);
        };
    }, []);

    // filter data by time
    useEffect(() => {
        let animationInterval;
        if (isPlaying && dataLoaded) {
            animationInterval = setInterval(() => {
                setCurrentTime(time => {
                    const newTime = time + 1000;
                    if (newTime > animationEndTime) {
                        return animationStartTime;
                    }
                    return newTime;
                });
            }, 200);
        }
        return () => clearInterval(animationInterval);
    }, [isPlaying, currentTime, dataLoaded, animationStartTime, animationEndTime]);

    const filteredData = currentTime !== null ? data.filter(d => d.timestamp <= currentTime) : [];

    // render data viz
    const staticLayers = [
        new ScatterplotLayer({
            id: 'scatterplot-layer-outline',
            data: cityData,
            getPosition: d => [d.coordinates.longitude, d.coordinates.latitude],
            getRadius: 4.50,  // size in pixels
            radiusUnits: 'pixels',  // specify radius in pixels
            pickable: false
        }),
        new ScatterplotLayer({
            id: 'scatterplot-layer',
            data: cityData,
            getPosition: d => [d.coordinates.longitude, d.coordinates.latitude],
            getRadius: 3.75,  // size of the dots
            getFillColor: [255, 150, 0],  // gold color
            radiusUnits: 'pixels',  // specify radius in pixels
            pickable: true,
            onHover: ({object, x, y}) => {
                if (object) {
                    setTooltip({
                        name: object.name,
                        x, y
                    });
                } else {
                    setTooltip(null);  // hide tooltip when not hovering over an object
                }
            }
        })
    ];
    const dynamicLayers = [
        ...(selectedCity ? [new ColumnLayer({
            id: 'column-layer',
            data: filteredData,
            getPosition: d => [d.geometry.coordinates[0], d.geometry.coordinates[1]],
            getElevation: d => d.properties.duration,
            getFillColor: d => rgbMap(d.properties.duration, maxDuration),
            radius: 10,
            pickable: true,
            autoHighlight: true,
            onHover: info => {
                if (info.object) {
                    setTooltipInfo({
                        x: info.x, // x position of the mouse
                        y: info.y, // y position of the mouse
                        object: info.object // data of the hovered column
                    });
                } else {
                    setTooltipInfo(null);
                }
            }
        })] : [])
    ];

    // render basemap
    return (
        <DeckGL
            style={{
                width: `calc(100vw - ${v.sidebarWidth})`,
                height: '100vh',
                margin: 0,
                marginLeft: v.sidebarWidth,
                padding: 0,
                overflow: 'hidden'
            }}
            initialViewState={viewport}
            onViewStateChange={({viewState, interactionState}) => {
                if (viewState.zoom > MAP_ZOOM + 2) {
                    viewState.zoom = MAP_ZOOM + 2;
                }
                setViewport(viewState);
                if (interactionState.isPanning || interactionState.isZooming || interactionState.isDragging) {
                    setUserInteracted(true);
                }
            }}
            controller={selectedCity !== null}  // enable map control only when a city is selected
            layers={selectedCity === null ? staticLayers : dynamicLayers}  // use static layers for world view, dynamic layers for city view
        >
            <Map
                mapStyle={mapStyle}
                mapboxAccessToken={REACT_APP_MAPBOX_TOKEN}
                attributionControl={false}
            />
            {tooltip && (
                <div style={{
                    position: 'absolute',
                    zIndex: 1,
                    pointerEvents: 'none',
                    left: tooltip.x,
                    top: tooltip.y-1,
                    color: 'white',
                    background: 'rgba(0, 0, 0, 0.67)',
                    padding: '5px',
                    borderRadius: '3px',
                    fontSize: '12px',
                }}>
                    {tooltip.name}
                </div>
            )}
            {selectedCity && <Minimap viewport={viewport} selectedCity={selectedCity} />}
            {selectedCity && tooltipInfo && (
                <div style={{
                    position: 'absolute',
                    zIndex: 1,
                    pointerEvents: 'none',
                    left: tooltipInfo.x,
                    top: tooltipInfo.y,
                    color: 'white',
                    background: 'rgba(0, 0, 0, 0.8)',
                    padding: '5px',
                    borderRadius: '3px',
                    fontSize: '12px',
                }}>
                    <div>Agency: {tooltipInfo.object.properties.agency}</div>
                    <div>Vehicle: {tooltipInfo.object.properties.vehicle_id}</div>
                    <div>Duration: {Math.floor(tooltipInfo.object.properties.duration / 60)} Minutes {tooltipInfo.object.properties.duration % 60} Seconds</div>
                    <div>Datetime: {new Date(tooltipInfo.object.properties.datetime * 1000).toLocaleString()} (UTC)</div>
                </div>
            )}
            {selectedCity && (
                <div style={{
                    position: 'absolute',
                    bottom: 0,
                    left: 0,
                    padding: '10px',
                    backgroundColor: 'rgba(255, 255, 255, 0.5)', // semi-transparent white
                    color: 'black',
                    fontSize: '12px'
                }}>
                    Hold Down "Shift" + Drag Mouse to Rotate
                </div>
            )}
            {selectedCity && (
                <RangeInput
                    min={animationStartTime}
                    max={animationEndTime}
                    value={currentTime}
                    isPlaying={isPlaying}
                    setIsPlaying={setIsPlaying}
                    onChange={(newValue) => {
                        setIsPlaying(false); // pause the animation
                        setCurrentTime(newValue);
                    }}
                />
            )}
        </DeckGL>
    );
}

// context minimap
function Minimap({ viewport, selectedCity }) {
    const { theme } = useContext(ThemeContext);
    const mapStyle = theme === 'dark' ? 'mapbox://styles/mapbox/dark-v9' : 'mapbox://styles/mapbox/light-v9';
    const minimapViewport = {
        ...viewport,
        longitude: selectedCity.coordinates.longitude,
        latitude: selectedCity.coordinates.latitude,
        zoom: 1,
        bearing: 0,
        pitch: 0
    };

    return (
        <div style={{
            position: 'absolute',
            bottom: 20, // 20 pixels from the bottom
            right: 20,  // 20 pixels from the right
            width: 200,
            height: 200,
            overflow: 'hidden', // stop spills outside the div
            border: '1px solid black' // add mini map border
        }}>
            <Map
                mapStyle={mapStyle}
                mapboxAccessToken={REACT_APP_MAPBOX_TOKEN}
                {...minimapViewport}
                attributionControl={false}
                interactive={false}
            >
            </Map>
            <div style={{
                position: 'absolute',
                top: '50%',
                left: '50%',
                transform: 'translate(-50%, -50%)',  // centers the loci
                height: 10,
                width: 10,
                backgroundColor: 'orange',
                borderRadius: '50%',
                border: '0.75px solid black'  // thin black border
            }} />
        </div>
    );
}

export default App;