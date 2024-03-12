import React from "react";
import { LargeTitle } from "../components/sidebar/styles";
import { TextContainer } from "../components/layout/styles";

const Data = () => {
    return (
        <TextContainer>
            <LargeTitle>Data</LargeTitle><br/>
            <h4>Realtime</h4>
            Idling data is provided realtime via Websocket (Socket.IO). Use the following endpoint and listen for events titled "events".<br/><br/>

            <i>Coming Soon...</i><br/><br/>

            <h4>Downloads</h4>
            Historical idling data can be downloaded as either GeoJSON or CSV. Use the following links to download the data.<br/><br/>

            <i>Coming Soon...</i><br/><br/>

            <h4>Database</h4>
            If advanced queries are required, the database can be accessed directly. Please contact us for more information.
        </TextContainer>
    );
};

export default Data;
