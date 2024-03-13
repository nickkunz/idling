import React from "react";
import { Route, Switch } from "react-router-dom";
import LiveMap from "./pages/Maps";
import About from "./pages/About";
import Data from "./pages/Data";

const Routes = ({ selectedCity }) => {
    return (
        <Switch>
            <Route exact path="/">
                <LiveMap selectedCity={selectedCity} />
            </Route>
            <Route exact path="/data">
                <Data />
            </Route>
            <Route exact path="/about">
                <About />
            </Route>
        </Switch>
    );
};

export default Routes;