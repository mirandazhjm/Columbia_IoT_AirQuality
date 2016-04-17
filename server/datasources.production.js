var dbconfig = require('../opsworks'); //[1] Include database connection data

module.exports = {
  'db': {
    'name': 'db',
    'connector': 'memory'
  },
  'air_monitor': {
    'host': dbconfig.db['host'],
    'port': dbconfig.db['port'],
    'database': dbconfig.db['database'],
    'username': dbconfig.db['username'],
    'password': dbconfig.db['password'],
    'name': 'air_monitor',
    'connector': 'mysql',
    'user': dbconfig.db['username']
  }
};