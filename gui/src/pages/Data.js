import React from "react";
import { StyledLink } from "../components/layout/styles";
import { LargeTitle } from "../components/sidebar/styles";
import { TextContainerWide } from "../components/layout/styles";

const Data = () => {
    return (
        <TextContainerWide>
            <LargeTitle>Data</LargeTitle><br/>
            <h3>Realtime</h3>
            Idling data is provided realtime via Websocket (Socket.IO). Use the following endpoint and listen for events titled <i>"events"</i>.<br/><br/>

            <code><b>https://idling-subset.redpebble-aeec30b4.westus.azurecontainerapps.io/</b></code><br/><br/>

            <h3>Downloads</h3>
            Historical idling data can be downloaded in either GeoJSON or CSV format. Use the following endpoint with the appropriate route and parameters to download the data.<br/><br/>

            <code><b>https://idling-read.redpebble-aeec30b4.westus.azurecontainerapps.io/</b></code><br/><br/>

            Specify one of the following routes:
            <ul>
                <li><code>/agency</code>: Retrieves transit agency table.</li>
                <li><code>/events</code>: Retrieves idling events table.</li>
                <li><code>/idle</code>: Joins agency table with events table.</li>
            </ul><br/>
            
            Parameters for each route can be specified as such:
            <ul>
                <li><code>format</code>: <code>geojson</code> or <code>csv</code> (e.g. <code>format=csv</code>).</li>
                <li><code>iata_id</code>: IATA code of transit agency (e.g. <code>iata_id=NYC</code>).</li>
            </ul><br/>

            Additional parameters that apply to the <code>/agency</code> route:
            <ul>
                <li><code>agency</code>: Name of transit agency.</li>
                <li><code>city</code>: City of transit agency.</li>
                <li><code>country</code>: Country of transit agency.</li>
                <li><code>region</code>: Region of transit agency.</li>
                <li><code>continent</code>: Continent of transit agency.</li>
            </ul><br/>

            Additional parameters that apply to <code>/events</code> and <code>/idle</code> routes:
            <ul>
                <li><code>vehicle_id</code>: Vehicle ID of idling events.</li>
                <li><code>route_id</code>: Route ID of idling events.</li>
                <li><code>trip_id</code>: Trip ID of idling events.</li>
                <li><code>datetime</code>: POSIX time of idling events.</li>
                <li><code>start_datetime</code>: Start POSIX time of idling events.</li>
                <li><code>end_datetime</code>: End POSIX time of idling events.</li>
                <li><code>duration</code>: Duration of idling events (seconds).</li>
                <li><code>min_duration</code>: Minimum duration of idling events (seconds).</li>
                <li><code>max_duration</code>: Maximum duration of idling events (seconds).</li>
            </ul><br/>

            Examples:<br/>
            <ul>
                <li>All idling events in New York City in CSV format: <code><b>https://idling-read.redpebble-aeec30b4.westus.azurecontainerapps.io/idle?format=csv&iata_id=NYC</b></code></li>
            </ul>
            <ul>
                <li>Idling events in Montreal longer than 5 minutes in GeoJSON format: <code><b>https://idling-read.redpebble-aeec30b4.westus.azurecontainerapps.io/idle?format=geojson&iata_id=YUL&min_duration=300</b></code></li>
            </ul>
            <ul>
                <li>Idling events in in Seattle on route identifier 100146 in CSV format: <code><b>https://idling-read.redpebble-aeec30b4.westus.azurecontainerapps.io/idle?format=csv&route_id=100146</b></code></li>
            </ul><br/>
            
            <h3>Database</h3>
            For advanced queries, the database can be accessed directly. Please see the <StyledLink href="/about">About</StyledLink> page to contact us for more information.
        </TextContainerWide>
    );
};

export default Data;