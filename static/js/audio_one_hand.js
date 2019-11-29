document.addEventListener("DOMContentLoaded", () => {

	const number = Math.floor(Math.random()*6);

        document.querySelector("#fingers").innerHTML = "<h2>Combien de doigts sont levés sur la main représentée à droite?</h2>";

	document.getElementById("goal").src = '/static/img/main'+number+'.png';

	//record microphone
	const recordAudio = () =>
		new Promise(async resolve => {
		  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
		  const mediaRecorder = new MediaRecorder(stream);
		  let audioChunks = [];
		  //if there is some new data block, we add it to the current recorded file
		  mediaRecorder.addEventListener('dataavailable', event => {
		    audioChunks.push(event.data);
		  });
		  //start mic
		  const start = () => {
		    // if we start again, we delete the previous chunks
		    audioChunks = [];
		    mediaRecorder.start();
		  };
		  //stop mic
		  const stop = () =>
		    new Promise(resolve => {
		      mediaRecorder.addEventListener('stop', () => {
		        // blob wraps the audiochunks
		        const audioBlob = new Blob(audioChunks);
		        //based on the data blocks, we create an audio file
		        const audioUrl = URL.createObjectURL(audioBlob);
		        const audio = new Audio(audioUrl);
		        //button play just play the static audio file
		        const play = () => audio.play();
		        resolve({ audioChunks, audioBlob, audioUrl, play });
		      });
		      mediaRecorder.stop();
		    });
		  resolve({ start, stop });
		});
	//const sleep = time => new Promise(resolve => setTimeout(resolve, time));
	//const savedAudioMessagesContainer = document.querySelector('#saved-audio-messages');

	//see the buttons div in the html page
	const recordButton = document.getElementById('record');
	const stopButton = document.getElementById('stop');
	const playButton = document.getElementById('play');
	const sendButton = document.getElementById('send');

	//Initialize the socket
	const ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
	const webSocket = new WebSocket(ws_scheme+ '://' + window.location.host +'/ws/audio/');

	this.webSocket.onmessage = function(e) {
            var data = JSON.parse(e.data);
            var message = data['message'];
            document.getElementById("c8").src = '/static/img/'+message+'.png';
	    if(message!=="error"){
		    if(number===parseInt(message)){
		        document.getElementById("res").src = '/static/img/valid.png'
		    }
		    else {
		        document.getElementById("res").src = '/static/img/wrong.png'
		    }
	    }
            else{

	    }
        };
    
        this.webSocket.onclose = function(e) {
            console.error('Socket closed');
        };

	let recorder; // see recordAudio() return
	let audio; // the final audio file

	//action record the mic
	recordButton.addEventListener('click', async () => {
		// disable other buttons when you press record	
		recordButton.setAttribute('disabled', true);
		stopButton.removeAttribute('disabled');
		playButton.setAttribute('disabled', true);
		sendButton.setAttribute('disabled', true);
		if (!recorder) {
		  recorder = await recordAudio();
		}
		recorder.start();
	});

	//action stop the recording
	stopButton.addEventListener('click', async () => {
		recordButton.removeAttribute('disabled');
		stopButton.setAttribute('disabled', true);
		playButton.removeAttribute('disabled');
		sendButton.removeAttribute('disabled');
		audio = await recorder.stop();
	});

	// action play the audio file to check if it's right
	playButton.addEventListener('click', () => {
		audio.play();
	});

	//save and send the file to the server
	sendButton.addEventListener('click', () => {
		// we load the audio file
		const reader = new FileReader();
		reader.readAsDataURL(audio.audioBlob);
		// we send it through the websocket
		reader.onload = () => {
		  const base64AudioMessage = reader.result.split(',')[1];
		  webSocket.send(JSON.stringify({
			'message': base64AudioMessage
		    }));
		  };
		});
});
