import React, { useContext, useState } from 'react';
import { FaMapMarkedAlt, FaChevronDown, FaDatabase } from "react-icons/fa";
import { MdOutlineAnalytics } from "react-icons/md";
import { ThemeContext } from "../../App";
import { useLocation } from "react-router-dom";
import {
    SDivider,
    SLink,
    SLinkContainer,
    SLinkIcon,
    SLinkLabel,
    SLinkNotification,
    SSidebar,
    STheme,
    SThemeLabel,
    SThemeToggler,
    SToggleThumb,
} from "./styles";

const Live = [
      { name: 'New York', iata_id: 'NYC', coordinates: { longitude: -74.0060, latitude: 40.7128 } },
      { name: 'Philadelphia', iata_id: 'PHL', coordinates: { longitude: -75.1652, latitude: 39.9526 } },
      { name: 'Washington D.C.', iata_id: 'DCA', coordinates: { longitude: -77.0369, latitude: 38.9072 } },
      { name: 'Boston', iata_id: 'BOS', coordinates: { longitude: -71.0589, latitude: 42.3601 } },
      { name: 'Pittsburgh', iata_id: 'PIT', coordinates: { longitude: -79.9959, latitude: 40.4406 } },
      { name: 'Los Angeles', iata_id: 'LAX', coordinates: { longitude: -118.2437, latitude: 34.0522 } },
      { name: 'San Francisco', iata_id: 'SFO', coordinates: { longitude: -122.41669, latitude: 37.7853 } },
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
      { name: 'Victoria', iata_id: 'YYJ', coordinates: { longitude: -123.3656, latitude: 48.4284 } },
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

const Sidebar = ({ onCitySelect }) => {
    const { pathname } = useLocation();
    const { setTheme, theme } = useContext(ThemeContext);
    const [isCitiesDropdownOpen, setIsCitiesDropdownOpen] = useState(false);

    const toggleCitiesDropdown = () => setIsCitiesDropdownOpen(prev => !prev);
    const handleCityClick = (city) => {
        if (onCitySelect) {
          onCitySelect(city.coordinates, city.iata_id); 
        }
        setIsCitiesDropdownOpen(false);
      };

    const linksArray = [
        {
            label: "Live",
            icon: <FaMapMarkedAlt/>,
            to: "/",
            notification: 0,

        },
        {
            label: "Data",
            icon: <FaDatabase />, 
            to: "/downloads",
            notification: 0,
        },
        {
            label: "About",
            icon: <MdOutlineAnalytics />,
            to: "/about",
            notification: 0,
        }
    ];

    // const secondaryLinksArray = [
    //     {
    //         label: "Developers",
    //         icon: <BsPeople />,
    //         to: "/developers",
    //         notification: 0,
    //     }
    // ];

    return (
        <SSidebar>
            Global Geolocated Realtime Data of Interfleet Urban Transit Bus Idling
            <SDivider />
            {linksArray.map(({ icon, label, notification, to, action }) => (
            <SLinkContainer key={label} isActive={pathname === to}>
                <SLink to={to} onClick={label === "Live" ? toggleCitiesDropdown : action || (() => {})}>
                    <SLinkIcon>{icon}</SLinkIcon>
                    <div style={{ display: 'flex', alignItems: 'center', width: '100%' }}>
                        <SLinkLabel style={{ marginRight: '8px' }}>{label}</SLinkLabel>
                        {label === "Live" && <FaChevronDown />}
                    </div>
                    {!!notification && <SLinkNotification>{notification}</SLinkNotification>}
                </SLink>
                {label === "Live" && isCitiesDropdownOpen && (
                    <div style={{ 
                        padding: '12px', 
                        maxHeight: '300px', 
                        overflowY: 'auto'
                    }}>
                        <style>
                            {`
                                div::-webkit-scrollbar {
                                    width: 15px; // Adjust the width of the scrollbar
                                }

                                div::-webkit-scrollbar-thumb {
                                    background: #888; // Color of the scrollbar thumb
                                }

                                div::-webkit-scrollbar-thumb:hover {
                                    background: #555; // Color when hovered
                                }
                            `}
                        </style>
                        {Live.map((city) => (
                        <p key={city.iata_id} style={{ margin: '5px 0' }} onClick={() => handleCityClick(city)}>
                            {city.name}
                        </p>
                        ))}
                    </div>
                    )}
                </SLinkContainer>
        ))}
            {/* <SDivider />
            {secondaryLinksArray.map((item, index) => (
                item.isDivider ? <SDivider key={index} /> : (
                    <SLinkContainer key={item.label}>
                        <SLink to="/">
                            <SLinkIcon>{item.icon}</SLinkIcon>
                            <SLinkLabel>{item.label}</SLinkLabel>
                        </SLink>
                    </SLinkContainer>
                )
            ))}  */}
            <SDivider />
            <STheme>
                <SThemeLabel>Dark Mode</SThemeLabel>
                <SThemeToggler
                    isActive={theme === "dark"}
                    onClick={() => setTheme((p) => (p === "light" ? "dark" : "light"))}
                >
                    <SToggleThumb style={theme === "dark" ? { right: "1px" } : {}} />
                </SThemeToggler>
            </STheme>
        </SSidebar>
    );
};

export default Sidebar;
