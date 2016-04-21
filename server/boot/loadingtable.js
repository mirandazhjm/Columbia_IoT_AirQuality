var ONE_HOUR = 60 * 60 * 1000; /* ms */
var SIX_HOUR = 6 * ONE_HOUR; /* ms */
var EIGHTEEN_HOUR = 18 * ONE_HOUR; /* ms */
var ONE_DAY = 24 * ONE_HOUR; /* ms */

module.exports = function (app) {    
    var appModels = ['air'];
    app.dataSources.air_monitor.isActual(appModels, function(err, actual) {
        if (!actual) {
            app.dataSources.air_monitor.autoupdate(appModels, function (err)
            { 
                if (err) throw (err);
                
                appModels.forEach(function(model)
                {
                    app.dataSources.air_monitor.discoverModelProperties(model, function (err, props) {
                        console.log(props);
                    });
                });
            });
        }
    }); 
    
};