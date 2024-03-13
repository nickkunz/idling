const GEOJSON_DATA = process.env.GEOJSON_DATA;

const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
    app.use(
        '/idle',
        createProxyMiddleware({
            target: GEOJSON_DATA,
            changeOrigin: true,
        })
    );
};
