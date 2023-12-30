// libraries
import React, { useState, useEffect, useCallback, useContext } from 'react';
import DeckGL from '@deck.gl/react';
import { Map } from 'react-map-gl';
import { ColumnLayer, ScatterplotLayer } from '@deck.gl/layers';
import { v } from '../styles/variables';
import { ThemeContext } from '../App';
import RangeInput from '../components/slider/Slider';

// params
const REACT_APP_MAPBOX_TOKEN = "pk.eyJ1Ijoibmlja2t1bnoiLCJhIjoiY2xwcTNrd3AzMTMwYjJrcjRmOGt2YmZjOCJ9.dDsSs9S8w2l7zAi05LaNhQ"
const MAP_ZOOM = 12;

// idling duration color map
function rgbMap(duration, maxDuration) {
    const intensity = duration / maxDuration;
    const greenComponent = 255 * (1 - intensity) * 0.67;  // reduce green
    return [255, greenComponent, 0];
}

// main app
function App({ selectedCity }) {
    const [data, setData] = useState([]);
    const [dataLoaded, setDataLoaded] = useState(false);
    const [currentTime, setCurrentTime] = useState(null);
    const [animationStartTime, setAnimationStartTime] = useState(null);
    const [animationEndTime, setAnimationEndTime] = useState(null);
    const [userInteracted, setUserInteracted] = useState(false);
    const [tooltipInfo, setTooltipInfo] = useState(null);
    const [isPlaying, setIsPlaying] = useState(true);
    const [viewport, setViewport] = useState({
        longitude: -73.9776,  // nyc lon
        latitude: 40.7420,  // nyc lat
        zoom: MAP_ZOOM,
        bearing: 60,
        pitch: 55
    });
    
    // map and sidebar style
    const { theme } = useContext(ThemeContext);
    const mapStyle = theme === 'dark' ? 'mapbox://styles/mapbox/dark-v9' : 'mapbox://styles/mapbox/light-v9';
    const maxDuration = Math.max(...data.map(d => d.properties.duration));

    // map rotation animation logic
    const animate = useCallback(() => {
        if (!userInteracted) {
            setViewport(v => ({
                ...v,
                bearing: v.bearing + 0.1
            }));
        }
    }, [userInteracted]);

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
                setIsPlaying(true); // Start the animation after data is loaded
            })
            .catch(error => console.error('Error fetching data:', error));
    };

    useEffect(() => {
        fetchData('/idle?iata_id=NYC');  // init loci
    }, []);

    // fetch data for selected city last 24 hours
    useEffect(() => {
        if (selectedCity) {
            const now = new Date();
            now.setUTCHours(now.getUTCHours() - 24);  // 24hrs ago in utc
            const roundedNow = Math.floor(now.getTime() / 1000);  // nearest second
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
            zoom: MAP_ZOOM  // reset zoom to default
            }));

            setCurrentTime(animationStartTime);
            setUserInteracted(false);
            setIsPlaying(true);  // start the animation
            }
        }, [selectedCity, animationStartTime])

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
    const layers = [
        new ColumnLayer({
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
        }),
        new ScatterplotLayer({
            id: 'scatterplot-layer',
            data: filteredData,
            getPosition: d => [d.geometry.coordinates[0], d.geometry.coordinates[1]],
            getRadius: 15,
            getFillColor: d => rgbMap(d.properties.duration, maxDuration),
            getElevation: d => d.properties.height,
            pickable: true,
            opacity: 1,
            stroked: true,
            lineWidthMinPixels: 2,
            getLineColor: d => rgbMap(d.properties.duration, maxDuration),
            autoHighlight: false
        })
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
                if (viewState.zoom < MAP_ZOOM - 2) {
                    viewState.zoom = MAP_ZOOM - 2;
                } else if (viewState.zoom > MAP_ZOOM + 2) {
                    viewState.zoom = MAP_ZOOM + 2;
                }
                setViewport(viewState);
                if (interactionState.isPanning || interactionState.isZooming || interactionState.isDragging) {
                    setUserInteracted(true);
                }
            }}
            controller={true}
            layers={layers}
        >
            <Map
                mapStyle={mapStyle}
                mapboxAccessToken={REACT_APP_MAPBOX_TOKEN}
                attributionControl={false}
            />
            <Minimap
                viewport={viewport}
                attributionControl={false}
            />
            {tooltipInfo && (
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
            <RangeInput
                min={animationStartTime}
                max={animationEndTime}
                value={currentTime}
                isPlaying={isPlaying}
                setIsPlaying={setIsPlaying}
                onChange={(newValue) => {
                    setIsPlaying(false); // Pause the animation
                    setCurrentTime(newValue);
                }}
            />
        </DeckGL>
    );
}

// context minimap
function Minimap({ viewport }) {
    const { theme } = useContext(ThemeContext);
    const mapStyle = theme === 'dark' ? 'mapbox://styles/mapbox/dark-v9' : 'mapbox://styles/mapbox/light-v9';
    const minimapViewport = {
        ...viewport,
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
                backgroundColor: 'red',
                borderRadius: '50%'
            }} />
        </div>
    );
}

export default App;
