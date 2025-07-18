const serverless = require('serverless-http');
const app = require('./_app');

module.exports = serverless(app);
