var status = require('./status');
module.exports = function(server) {
  // Install a `/` route that returns server status
  var router = server.loopback.Router();
  router.get('/', status());
  server.use(router);
};
