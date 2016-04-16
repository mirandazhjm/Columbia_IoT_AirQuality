var loopback = require('loopback');
var boot = require('loopback-boot');

var app = module.exports = loopback();
var dbconfig = require('./opsworks'); //[1] Include database connection data

module.exports = {
  'db': {
    'name': 'db',
    'connector': 'memory'
  },
  'mysql': {
    'host': dbconfig.db['host'],
    'port': dbconfig.db['port'],
    'database': dbconfig.db['database'],
    'username': dbconfig.db['username'],
    'password': dbconfig.db['password'],
    'name': 'mysql',
    'connector': 'mysql',
    'user': dbconfig.db['username']
  }
};

app.start = function() {
  // start the web server
  return app.listen(function() {
    app.emit('started');
    var baseUrl = app.get('url').replace(/\/$/, '');
    console.log('Web server listening at: %s', baseUrl);
    if (app.get('loopback-component-explorer')) {
      var explorerPath = app.get('loopback-component-explorer').mountPath;
      console.log('Browse your REST API at %s%s', baseUrl, explorerPath);
    }
  });
};

// Bootstrap the application, configure models, datasources and middleware.
// Sub-apps like REST API are mounted via boot scripts.
boot(app, __dirname +'/server', function(err) {
  if (err) throw err;

  // start the server if `$ node server.js`
  if (require.main === module)
    app.start();
});
