//INSPIIIIREDDDDDDDDDDD

window.app = window.app || {};

// strict mode wrapper
(function defineAppUi(app) {
    'use strict';
    
    var SENSOR_DATA_UPDATE_INTERVAL = 500
    var   DEVICE_RADIUS = 180
    var  canvas = document.getElementById('app-canvas')
	 var   context = canvas.getContext('2d')
	 var   counter = document.getElementById('counter')
	 
    var websocket = new WebSocket('ws://192.168.136.53:8080');
    
    
    websocket.onopen = function(event) {
        console.log("WebSocket connection established.");
    };

    websocket.onerror = function(event) {
        console.error("WebSocket error:", event);
    };

    websocket.onclose = function(event) {
        console.log("WebSocket connection closed.");
    };
    
    
    function sendLightValue(lightValue) {
        websocket.send(lightValue);
    }
    
    function onSensorValueReceived(sensorData) {
        counter.innerText = sensorData.lightLevel + ' lx';
        console.log(counter.innerText);
        sendLightValue(counter.innerText.toString());
    }
    
    function updateView() {
        app.model.getSensorValue(onSensorValueReceived);
    }
    
    function init() {

        canvas.width = DEVICE_RADIUS * 2;
        canvas.height = DEVICE_RADIUS * 2;

        
        



        window.setInterval(updateView, SENSOR_DATA_UPDATE_INTERVAL);
    }

    app.ui = {
        init: init
    };

}(window.app));