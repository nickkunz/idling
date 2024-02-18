import React from "react";
import { Route, Switch } from "react-router-dom";
import LiveMap from "./pages/Maps";

const Routes = ({ selectedCity }) => {
    return (
        <Switch>
            <Route exact path="/">
                <LiveMap selectedCity={selectedCity} />
            </Route>
            <Route exact path="/about">
                <h1>Coming Soon... </h1>
            </Route>
            <Route exact path="/downloads">
                <h1>Coming Soon... </h1>
            </Route>
        </Switch>
    );
};

export default Routes;
