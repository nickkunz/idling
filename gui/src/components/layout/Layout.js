import React, { useState } from 'react';
import Sidebar from '../sidebar/Sidebar';
import { SLayout, SMain } from './styles';
import Routes from '../../routes';

const Layout = () => {
    const [selectedCity, setSelectedCity] = useState(null);
    const handleCitySelect = (coordinates, iataId) => {
        setSelectedCity({ coordinates, iataId });
    };

    return (
        <SLayout>
            <Sidebar onCitySelect={handleCitySelect} />
            <SMain>
                <Routes selectedCity={selectedCity} />
            </SMain>
        </SLayout>
    );
};

export default Layout;
