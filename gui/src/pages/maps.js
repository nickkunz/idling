// libraries
import React, { useState, useEffect, useCallback, useContext } from 'react';
import DeckGL from '@deck.gl/react';
import { Map } from 'react-map-gl';
import { ColumnLayer, ScatterplotLayer } from '@deck.gl/layers';
import { v } from '../styles/variables';
import { ThemeContext } from '../App';
import RangeInput from '../components/slider/Slider';
import 'mapbox-gl/dist/mapbox-gl.css';

// params
const REACT_APP_MAPBOX_TOKEN = process.env.REACT_APP_MAPBOX_TOKEN;
const MAP_ZOOM = 12;

// idling duration color map
function rgbMap(duration, maxDuration) {
    const intensity = duration / maxDuration;
    const greenComponent = 255 * (1 - intensity) * 0.67;  // reduce green
    return [255, greenComponent, 0];
}

// main app
function LiveMap({ selectedCity }) {
    const [data, setData] = useState([]);
    const [dataLoaded, setDataLoaded] = useState(false);
    const [currentTime, setCurrentTime] = useState(null);
    const [animationStartTime, setAnimationStartTime] = useState(null);
    const [animationEndTime, setAnimationEndTime] = useState(null);
    const [userInteracted, setUserInteracted] = useState(false);
    const [tooltipInfo, setTooltipInfo] = useState(null);
    const [isPlaying, setIsPlaying] = useState(false);
    const [viewport, setViewport] = useState({
        longitude: -74.0060,  // nyc lon
        latitude: 40.7128,  // nyc lat
        zoom: MAP_ZOOM,
        bearing: 60,
        pitch: 55
    });
    
    // map and sidebar style
    const { theme } = useContext(ThemeContext);
    const mapStyle = theme === 'dark' ? 'mapbox://styles/mapbox/dark-v9' : 'mapbox://styles/mapbox/light-v9';
    const maxDuration = data.length > 0 ? Math.max(...data.map(d => d.properties.duration)) : 1;  // avoid division by zero

    // map rotation animation logic
    const animate = useCallback(() => {
        if (!userInteracted) {  // only animate if a city is selected
            setViewport(v => ({
                ...v,
                bearing: v.bearing + 0.1
            }));
        }
    }, [userInteracted]);

    useEffect(() => {
        const interval = setInterval(animate, 200);  // update every 200 ms
        return () => clearInterval(interval);
    }, [animate]);

    // fetch data from server
    const fetchData = (url) => {
        setIsPlaying(false);
        setCurrentTime(null);
        setDataLoaded(false);
        const fullUrl = `/idle${url}`;  // rev proxy request through nginx
        console.log(`Fetching data from: ${fullUrl}`);
    
        fetch(fullUrl)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(fetchedData => {
                if (fetchedData.features && fetchedData.features.length > 0) {
                    const timestamps = fetchedData.features.map(d =>
                        new Date(d.properties.datetime).getTime()
                    );
                    const minTime = Math.min(...timestamps);
                    const maxTime = Math.max(...timestamps);
    
                    setData(fetchedData.features.map(d => ({
                        ...d,
                        timestamp: new Date(d.properties.datetime).getTime()
                    })));
                    setAnimationStartTime(minTime);
                    setAnimationEndTime(maxTime);
                    setCurrentTime(minTime);
                    setIsPlaying(true);  // start the animation after data is loaded
                } else {
                    // no data available
                    setData([]);
                    setAnimationStartTime(null);
                    setAnimationEndTime(null);
                    setCurrentTime(null);
                    setIsPlaying(false);  // stop the animation
                }
                setDataLoaded(true);
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                setData([]);
                setAnimationStartTime(null);
                setAnimationEndTime(null);
                setCurrentTime(null);
                setIsPlaying(false);  // stop the animation
                setDataLoaded(true);
            });
    };

    // posix timestamp for n hours ago in UTC (sec)
    const fetchDataHours = (hours) => {
        const nowUTC = new Date().getTime();  // current time in ms (UTC)
        const startUTC = nowUTC - (hours * 60 * 60 * 1000);  // subtract n hours in ms
        return Math.floor(startUTC / 1000); // convert to sec
    };

    // fetch data in nyc for last n hours
    useEffect(() => {
        const startTimestamp = fetchDataHours(96);
        fetchData(`?iata_id=NYC&start_datetime=${startTimestamp}`);  // init loci
    }, []);

    // fetch data in selected city for last n hours
    useEffect(() => {
        if (selectedCity) {
            const startTimestamp = fetchDataHours(96);
            fetchData(`?iata_id=${selectedCity.iataId}&start_datetime=${startTimestamp}`); 
        } 
    }, [selectedCity])

    // animation logic
    useEffect(() => {
        let interval;

        // animate only if playing, data is loaded, and there is data
        if (isPlaying && dataLoaded && data.length > 0) {
            interval = setInterval(() => {
                setCurrentTime(time => {
                    const newTime = time + 1000;  // increment every second
                    if (newTime > animationEndTime) {
                        return animationStartTime;  // reset for infinite loop
                    }
                    return newTime;
                });
            }, 200);  // update every 200 ms
        }
        return () => clearInterval(interval);
    }, [isPlaying, dataLoaded, data.length, currentTime, animationStartTime, animationEndTime]);

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
            {dataLoaded && data.length > 0 && (
                <RangeInput
                    min={animationStartTime}
                    max={animationEndTime}
                    value={currentTime}
                    isPlaying={isPlaying}
                    setIsPlaying={setIsPlaying}
                    onChange={(newValue) => {
                        setIsPlaying(false);
                        setCurrentTime(newValue);
                    }}
                />
            )}
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
                transform: 'translate(-50%, -50%)',  // centers the marker
                height: 10,
                width: 10,
                backgroundColor: 'orange',
                borderRadius: '50%',
                border: '1px solid black' // Add black outline
            }} />
        </div>
    );
}

export default LiveMap;
