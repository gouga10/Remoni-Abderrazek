(function () {
	var	parsedIPs
    var defaultAddress = 'ws://192.168.139.53:8080';
    var websocket;
    var start=0;
    var selectedIP=''
    function connectWebSocket(ipAddress) {
        var url = 'ws://' + ipAddress + ':8080';
        websocket = new WebSocket(url);
        
        websocket.onopen = function(event) {
            console.log("WebSocket connection established.");
            //tizen.humanactivitymonitor.start('SLEEP_MONITOR',onsuccessCB ,onerrorCB);
        	tizen.humanactivitymonitor.start('HRM',onchangedHR);
        	accelerometerSensor = tizen.sensorservice.getDefaultSensor('LINEAR_ACCELERATION');
        	accelerometerSensor.start(accelerometer_onsuccessCB);
        };

        websocket.onerror = function(event) {
            console.error("WebSocket error:", event);
        };

        websocket.onclose = function(event) {
            console.log("WebSocket connection closed.");
        };
    }
    

    	
    function saveIPAddressToFile(ip) {


    	
    	/* Opening file for read - this code assumes that there is */
    	/* a file named "file" in documents directory. */
    	try{
    	var fileHandleRead = tizen.filesystem.openFile("documents/file", "r");}
    	catch(err) {
    		var fileHandleWrite = tizen.filesystem.openFile("documents/file", "w");
    		console.log("File opened for writing");
    		fileHandleWrite.writeString("");
    		var fileHandleRead = tizen.filesystem.openFile("documents/file", "r");
    		}
    	/* ReadStringSuccessCallback should be executed. */
    	fileHandleRead.readStringNonBlocking(
    	    function(output)
    	    {
    	    	
    	    	
    	    	if (output == ''){
    	    		var fileHandleWrite = tizen.filesystem.openFile("documents/file", "w");
        	    	fileHandleWrite.writeStringNonBlocking(output+'#'+ip+'#',
        	    	function(bytesCount)
        	    	    {
        	    	      console.log("Number of bytes written: " + bytesCount);
        	    	    },
        	    	function(error)
        	    	    {
        	    	      console.log(error);
        	    	    });
        	    	console.log("File content: "+output +'#'+ip+'#');
    		
    	    	}
    	    	
    	    	
    	    	else{
    	    	var fileHandleWrite = tizen.filesystem.openFile("documents/file", "w");
    	    	fileHandleWrite.writeStringNonBlocking(output+ip+'#',
    	    	function(bytesCount)
    	    	    {
    	    	      console.log("Number of bytes written: " + bytesCount);
    	    	    },
    	    	function(error)
    	    	    {
    	    	      console.log(error);
    	    	    });
    	    	console.log("File content: " + output+ip+'#');}
    	    },
    	    function(error)
    	    {
    	      console.log(error);
    	    });
    	fileHandleRead.closeNonBlocking(
    	    function()
    	    {
    	      console.log("File handle closed");
    	    },
    	    function(error)
    	    {
    	      console.log(error);
    	    });
    }
    
    // Function to connect using the default address
    function useDefaultIp() {
    	websocket = new WebSocket(defaultAddress);
        websocket.onopen = function(event) {
            console.log("WebSocket connection established.");
            tizen.humanactivitymonitor.start('SLEEP_MONITOR',onsuccessCB ,onerrorCB);
        	tizen.humanactivitymonitor.start('HRM',onchangedHR);
        	accelerometerSensor = tizen.sensorservice.getDefaultSensor('LINEAR_ACCELERATION');
        	accelerometerSensor.start(accelerometer_onsuccessCB);
        };

        websocket.onerror = function(event) {
            console.error("WebSocket error:", event);
        };

        websocket.onclose = function(event) {
            console.log("WebSocket connection closed.");
        };
    }
    
    // Function to connect with user-defined address
    function connectWithUserAddress() {
        var ipAddress = document.getElementById('ipAddress').value.trim();
        if (ipAddress) {
        	
            connectWebSocket(ipAddress);
            saveIPAddressToFile(ipAddress);
            
            
        } else {
        	
        	console.log(' IP problem ')        }
        
    }

    // Event listener for the Connect button
    

    // Connect using the default address initially
    
    

    
    function sendWeb(data) {
    	console.log(websocket)
        websocket.send(data);
    }
	
	/*****************************  Heart Rate  *************************************************/

	var heart =document.getElementById('heart');
	var heartRate=0
	function onchangedHR(hrmInfo)
	{
		heart.innerHTML=hrmInfo.heartRate;
		//console.log(hrmInfo);
		heartRate=hrmInfo.heartRate;
		
		const now = new Date();
		
		const minutes = now.getMinutes();
		if (minutes == 29){
			if (UpdateHeartRate==true){
				sendWeb(JSON.stringify({heart: heartRate}));
				UpdateHeartRate=false
			}
			}
			
		else if (minutes == 59){
			if (UpdateHeartRate==true){
				sendWeb(JSON.stringify({heart: heartRate}));
				UpdateHeartRate=false;
			}
		}
		else {
			UpdateHeartRate=true;
		}
		
		
		
	}
	/*****************************    Heart Rate   ************************************************/
	/*****************************    Sleep   ************************************************/
	var sleep =document.getElementById('sleep');
	var sleep_status='';

	function onchangedCB(sleepInfo) {
	    //console.log('Sleep status: ' + sleepInfo.status);
	    //console.log('Timestamp: ' + sleepInfo.timestamp + ' milliseconds');
	    sleep.innerHTML=sleepInfo.status;
	    sleep_status=sleepInfo.status;
	   
	}
	function onsuccessCB(sleepInfo) {
		console.log('Sleep status: ' + sleepInfo.status);
	    console.log('Timestamp: ' + sleepInfo.timestamp + ' milliseconds');
	    sleep.innerHTML=sleepInfo.status;
	    sleep_status=sleepInfo.status;
	}

	function onerrorCB(error) {
	    console.log('Error occurred: ' + error.message);
	}

	
	
	
	/*****************************    sleep   ************************************************/

	/*****************************    Accelerometer   ************************************************/
	
	var ax,ay,az = 0;
	var axh =document.getElementById('axh');
	var ayh =document.getElementById('ayh');
	var azh =document.getElementById('azh');

	var accelerometerSensor;

	var accelerometerRateEl;
	
	
	var Data = {};
	
	function accelerometer_onsuccessCB()
	{
	  console.log("Accelerometer sensor started succesfully");
	  setInterval(readAccelerometerData, 312);

	  
	}
	function readAccelerometerData() {
	    accelerometerSensor.getLinearAccelerationSensorData(accelerometer_onGetSuccessCB, accelerometer_onerrorCB);
	}
	
	function accelerometer_onGetSuccessCB(sensorData) {
		
		ax = (sensorData.x).toFixed(2);
		ay = (sensorData.y).toFixed(2);
		az = (sensorData.z).toFixed(2);
	   /* console.log("######## Get accelerometer sensor data ########");
	    console.log("ax: " + sensorData.x);
	    console.log("ay: " + sensorData.y);
	    console.log("az: " + sensorData.z);*/
	  
	    accelerometerSensor.setChangeListener(accelerometer_onchangedCB);
	}
	


	
	function ManageTables(table1,table2,data,send_cloud) {
	    i=table1.length;
	    j=table2.length;
	        if (Table1IsFull==false){
	            if(Table1IsEmpty){
	                if (Table2IsFull)
	                {
	                    const lastTransferedDataRows = table2.slice(-TransferedData);
	                    Array.prototype.push.apply(table1, lastTransferedDataRows);
	                    console.log('Number of rows in Table 1: ${table1.length}');
	                    Table1IsEmpty=false;
	    
	                }
	            }
	            
	            
	            if (i < NumberOfRows) {
	                const newRow = data;
	                table1.push(newRow);
	                //console.log(`Number of rows in Table 1: ${table1.length}`);
	                
	                        } 
	            if(i==NumberOfRows)
	            {
	            	if (sendcloud)
                	{
	            	
                	sendWeb(JSON.stringify({ table: table1}));
                	sendcloud=false;
                	}
	                Table1IsFull=true;
	                table2.length = 0;
	                Table2IsFull=false;
	                Table2IsEmpty=true;
	                
	            }
	        }
	        
	        
	        
	        else {
	            if (Table2IsFull==false) {
	                if(Table2IsEmpty){
	                    if (Table1IsFull)
	                        {
	                        const lastTransferedDataRows = table1.slice(-TransferedData);
	                        Array.prototype.push.apply(table2, lastTransferedDataRows);
	                        console.log('Number of rows in Table 2: ${table2.length}');
	                        Table2IsEmpty=false;
	           
	                        }
	                }
	                
	                if (j < NumberOfRows) {
	                const newRow = data;
	                table2.push(newRow);
	                //console.log(`Number of rows in Table 2: ${table2.length}`);
	                
	                        } 
	                if(j==NumberOfRows)
	                {
	                	if (sendcloud)
	                	{
	                	

	                	sendWeb(JSON.stringify({table:table2}));
	                	sendcloud=false;
	                	
	                	}
	                    Table2IsFull=true;
	                    table1.length = 0;
	                    Table1IsFull=false;
	                    Table1IsEmpty=true;
	                    
	                }  
	                
	            }
	            
	        }

	        
	}
	

	function accelerometer_onchangedCB(sensorData) {
		
		ax = sensorData.x.toFixed(2);
		ay = sensorData.y.toFixed(2);
		az = sensorData.z.toFixed(2);
		
	    
	    
		/*console.log("######## Get accelerometer sensor data ########");
		console.log("ax: " + sensorData.x);
		console.log("ay: " + sensorData.y);
		console.log("az: " + sensorData.z);*/
		axh.innerHTML=ax;
		ayh.innerHTML=ay;
		azh.innerHTML=az;
		Acceleration1= {
            "ax": ax,
            "ay": ay,
            "az": az }
		
		Data= {"HeartRate1":heartRate ,
				"Sleep_status":sleep_status,
				"Acceleration1":Acceleration1};
		
		if (ax>1)   {
			sendcloud=true
		}
		if (ay>1) {
			sendcloud=true
		}
		if (az>1){
			sendcloud=true
		}
		console.log(sendcloud);
		console.log('Number of rows in Table 1: ' + table1.length);
		console.log('Number of rows in Table 2: ' + table2.length);
		ManageTables(table1, table2,Acceleration1,sendcloud);

			    /* Convert object to JSON string
			    var jsonData = JSON.stringify(Data);

			    // Log JSON data
			    console.log(jsonData);
				sendWeb(jsonData.toString());*/

	    
	}

	function accelerometer_onerrorCB(error) {
	    console.log("Error name:"+error.name + ", message: "+error.message);
	}
	

	function stopAccelerometer(){
		accelerometerSensor.stop();
	}
	
	/*****************************    Accelerometer   ************************************************/

	
	function parseIPAddresses(ipString) {
	    // Split the input string by '#' to get individual IP addresses
	    var ipAddresses = ipString.split('#').filter(Boolean);

	    // Return the array of parsed IP addresses
	    return ipAddresses;
	}
	
	
	
	
	function EmptyList() {
	var fileHandleWrite = tizen.filesystem.openFile("documents/file", "w");
	console.log("File opened for writing");
	fileHandleWrite.writeString("#");
	console.log("file is Empty");
	fileHandleWrite.close();
	 window.location.href = "index.html";
	}
	   function connectSelected(){
	    	
	    	var selectedIP = selectElement.value;
	    	connectWebSocket(selectedIP)
	    }
	/*****************************    APP   ************************************************/
	
	   
   TransferedData=100;
   const table1 = [];
   const table2 = [];
   NumberOfRows=680;
   let sendcloud=false;
   let UpdateHeartRate= true;
   let Table2IsEmpty= true;
   let Table1IsEmpty = true;
   let Table2IsFull = false;
   let Table1IsFull = false;  
	   
	   
	document.getElementById('connectBtn').addEventListener('click', connectWithUserAddress);
    document.getElementById('defaultIpBtn').addEventListener('click', useDefaultIp);
    
	document.getElementById('EmptyBtn').addEventListener('click', EmptyList);
    var selectElement = document.getElementById("ipSelect");

    var fileHandleRead = tizen.filesystem.openFile("documents/file", "r");
    /* ReadStringSuccessCallback should be executed. */
    fileHandleRead.readStringNonBlocking(
        function(output)
        {
         	parsedIPs = parseIPAddresses(output);
            parsedIPs.forEach(function(ip) {
                var option = document.createElement("option");
                option.text = ip;
                option.value = ip;
                selectElement.add(option);
            });

        },
        function(error)
        {
          console.log(error);
        });
    fileHandleRead.closeNonBlocking(
        function()
        {
          console.log("File handle closed");
        },
        function(error)
        {
          console.log(error);
        });



 
  
    
    
	document.getElementById('SelectBtn').addEventListener('click', connectSelected);

    

    
	/*****************************    APP   ************************************************/

	window.addEventListener("tizenhwkey", function (ev) {
		var activePopup = null,
			page = null,
			pageId = "";

		if (ev.keyName === "back") {
			activePopup = document.querySelector(".ui-popup-active");
			page = document.getElementsByClassName("ui-page-active")[0];
			pageId = page ? page.id : "";

			if (pageId === "main" && !activePopup) {
				try {
					tizen.application.getCurrentApplication().exit();
					
				} catch (ignore) {
				}
			} else {
				window.history.back();
			}
		}
	});

}());