let counter = {
	 	
	// 'remove' the background of an image
	computeDiff: function (img, background){
		
		let l = img.data.length/4;
		
		for (let i = 0; i < l; i++) {
			let r = img.data[i * 4 ];
			let r_bg = background.data[i*4];
			let g = img.data[i * 4 + 1];
			let g_bg = background.data[i * 4 + 1];
			let b = img.data[i * 4 + 2];
			let b_bg = background.data[i * 4 + 2];
			if ( (r-r_bg)**2 + (g-g_bg)**2 + (b-b_bg)**2 > this.threshold){
				background.data[i*4]=255;
				background.data[i*4+1]=255;
				background.data[i*4+2]=255;
			}
			else {
				background.data[i*4]=0;
				background.data[i*4+1]=0;
				background.data[i*4+2]=0;
			}
		}
		
		return background;
	},
	
	computeFrame: function() {
	  
	  var canvas = document.createElement("canvas");
	  canvas.width = this.video.videoWidth;
	  canvas.height = this.video.videoHeight;
	  var ctxcanv = canvas.getContext('2d');
	  ctxcanv.drawImage(this.video, 0, 0, this.video.videoWidth, this.video.videoHeight);
	  
	  let frame_left = ctxcanv.getImageData(0, 0, this.width, this.height);
      this.ctx1.putImageData(frame_left, 0, 0);
	  
      let frame_right = ctxcanv.getImageData(this.width, 0, this.video.videoWidth, this.height);
      this.ctx5.putImageData(frame_right, 0, 0);
	  
	  if(this.backgroundSaved){
		this.ctx3.putImageData(this.computeDiff(frame_left, this.ctx2.getImageData(0, 0, this.width, this.height)), 0, 0);
		this.ctx7.putImageData(this.computeDiff(frame_right, this.ctx6.getImageData(0, 0, this.width*2, this.height)), 0, 0);
	  }
	  
      return;
    },
	
    doLoad: function() {
      this.video = document.getElementById("video");
      this.c1 = document.getElementById("c1");
      this.ctx1 = this.c1.getContext("2d");
      this.c2 = document.getElementById("c2");
      this.ctx2 = this.c2.getContext("2d");
	  this.c3 = document.getElementById("c3");
      this.ctx3 = this.c3.getContext("2d");
      this.c4 = document.getElementById("c4");
      this.ctx4 = this.c4.getContext("2d");
	  this.c5 = document.getElementById("c5");
      this.ctx5 = this.c5.getContext("2d");
      this.c6 = document.getElementById("c6");
      this.ctx6 = this.c6.getContext("2d");
	  this.c7 = document.getElementById("c7");
      this.ctx7 = this.c7.getContext("2d");
      this.c8 = document.getElementById("c8");
      this.ctx8 = this.c8.getContext("2d");
	  this.backgroundSaved = false;
	  this.threshold = 2000;
      let self = this;
	  this.width = self.video.videoWidth/2;
	  this.height = self.video.videoHeight/2;
      this.video.addEventListener("play", function() {
          self.width = self.video.videoWidth / 2;
          self.height = self.video.videoHeight / 2;
          self.timerCallback();
        }, false);
    },
	
	initSocket: function(){
    	var userName = "room";

        this.webSocket = new WebSocket('ws://' + window.location.host +'/ws/picture/' + userName + '/');
		
        console.log(this.webSocket);
        
        this.webSocket.onmessage = function(e) {
            var data = JSON.parse(e.data);
            var message = data['message'];
            console.log(message);
        };
    
        this.webSocket.onclose = function(e) {
            console.error('Web socket closed unexpectedly');
        };
    },
	
	initVideo: function(){
		var video = document.querySelector("#video");
		if (navigator.mediaDevices.getUserMedia) {       
			navigator.mediaDevices.getUserMedia({video: true})
		  .then(function(stream) {
			video.srcObject = stream;
		  })
		  .catch(function(error) {
			console.log("Something went wrong with the webcam!");
		  });
		}
	},
	
	// save two pictures of reference
	saveBackground: function(){
	  var canvas = document.createElement("canvas");
	  canvas.width = this.video.videoWidth;
	  canvas.height = this.video.videoHeight;
	  var ctxcanv = canvas.getContext('2d');
	  ctxcanv.drawImage(this.video, 0, 0, this.video.videoWidth, this.video.videoHeight);
	  
	  let frame_left = ctxcanv.getImageData(0, 0, this.width, this.height);
      this.ctx2.putImageData(frame_left, 0, 0);
	  
      let frame_right = ctxcanv.getImageData(this.width, 0, this.video.videoWidth, this.height);
      this.ctx6.putImageData(frame_right, 0, 0);
	  
	  this.backgroundSaved = true;
	  
      return;
	},
	
	// send the computed pictures to the server -> ML to count the number of fingers -> response
    sendPicture: function(){
        if(this.backgroundSaved){
            var msg = this.c7.toDataURL('image/png').replace('data:image/png;base64,','');
            this.webSocket.send(JSON.stringify({
                'message': msg
            }));
			msg = this.c3.toDataURL('image/png').replace('data:image/png;base64,','');
            this.webSocket.send(JSON.stringify({
                'message': msg
            }));
        }
    },
    
    timerCallback: function() {
      if (this.video.paused || this.video.ended) {
        return;
      }
      this.computeFrame();
      let self = this;
      setTimeout(function () {
          self.timerCallback();
        }, 0);
    }
  };

document.addEventListener("DOMContentLoaded", () => {
	
	//initialize the video
	counter.initVideo();
	
	//initialize the socket
	counter.initSocket();
	
	// launch the image processing
	counter.doLoad();

});