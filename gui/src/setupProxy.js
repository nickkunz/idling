const REACT_APP_GEOJSON_DATA = process.env.REACT_APP_GEOJSON_DATA;

const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
    app.use(
        '/idle',
        createProxyMiddleware({
            target: REACT_APP_GEOJSON_DATA,
            changeOrigin: true,
        })
    );
};