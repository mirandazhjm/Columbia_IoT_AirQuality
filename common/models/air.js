var request = require('request');

module.exports = function(Air) {
	Air.observe('before save', function updateTimestamp(data, next) {


	if (data.instance) {

	var message = data.instance;

	data.instance.timestamp = new Date();

	} else {

	message = data.data;

	data.data.timestamp = new Date();

	}





	var payload = {

	'field1': message.temperature,

	'field2': message.humidity,

	'field3': message.co2,

	'field4': message.voc,

	'api_key': 'EHR5ZBYEZ9MF3T8X'

	};



	var options = {

	method: 'post',

	body: payload, // Javascript object

	json: true, // Use,If you are sending JSON data

	url: 'https://api.thingspeak.com/update.json',

	}



	request(

	options,

	function (error, response, body) {

	if (!error && response.statusCode == 200) {

	console.log(body)

	}

	}

	);





	next();

	});

};
