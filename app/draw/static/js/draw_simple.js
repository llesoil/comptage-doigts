let draw =  {
	addClick:function(x, y, dragging){
		this.clickX.push(x);
		this.clickY.push(y);
		this.clickDrag.push(dragging);
	},
        clear:function(){
		this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
		this.clickX = new Array();
		this.clickY = new Array();
		this.clickDrag = new Array();
	},
        init:function(){
		self=this;
		this.clickX = new Array();
		this.clickY = new Array();
		this.clickDrag = new Array();
		this.paint;
		this.canvasDiv = document.getElementById('canvasDiv');
		this.canvas = document.createElement('canvas');
		this.canvas.setAttribute('width', "140");
		this.canvas.setAttribute('height', "140");
		this.canvas.setAttribute('id', 'canvas');
		this.canvasDiv.appendChild(this.canvas);
                this.offsetLeft=this.offsetLeft+100;
		if(typeof G_vmlCanvasManager !== 'undefined') {
		    this.canvas = G_vmlCanvasManager.initElement(this.canvas);
		}
		this.context = canvas.getContext("2d");

		$('#canvas').mousedown(function(e){
		    var mouseX = e.pageX - this.offsetLeft;
		    var mouseY = e.pageY - this.offsetTop;
		     
		    this.paint = true;
		    draw.addClick(e.pageX - this.offsetLeft, e.pageY - this.offsetTop);
		    draw.redraw();
		});
	 
		$('#canvas').mousemove(function(e){
		    if(this.paint){
			draw.addClick(e.pageX - this.offsetLeft, e.pageY - this.offsetTop, true);
			draw.redraw();
		    }
		});      
	 
		$('#canvas').mouseup(function(e){
		    this.paint = false;
		});
	 
		$('#canvas').mouseleave(function(e){
		    this.paint = false;
		});
	},
	initSocket: function(number){
	    	
	    	var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
	    	
		this.webSocket = new WebSocket(ws_scheme+ '://' + window.location.host +'/ws/draw/');
	
		console.log(this.webSocket);
	
		this.webSocket.onmessage = function(e) {
		    var data = JSON.parse(e.data);
		    var message = data['message'];
		    var predictedValue = message;
		    //document.getElementById("c8").src = '/static/img/'+predictedValue+'.png';
                    console.log(predictedValue);
		    if(number===parseInt(predictedValue)){
			document.getElementById("res").src = '/static/img/valid.png'
		    }
		    else {
			document.getElementById("res").src = '/static/img/wrong.png'
		    }
		};
	    
		this.webSocket.onclose = function(e) {
		    console.error('Socket closed');
		};
	    },
	redraw:function(){
        	this.context.clearRect(0, 0, this.context.canvas.width, this.context.canvas.height); // Clears the canvas
     
        	this.context.strokeStyle = "#333";
        	this.context.lineJoin = "round";
        	this.context.lineWidth = 8;
     
        	for(var i=0; i < this.clickX.length; i++) {       
        		this.context.beginPath();
        		if(this.clickDrag[i] && i){
            			this.context.moveTo(this.clickX[i-1], this.clickY[i-1]);
        		}else{
            			this.context.moveTo(this.clickX[i]-1, this.clickY[i]);
        		}
        		this.context.lineTo(this.clickX[i], this.clickY[i]);
        		this.context.closePath();
        		this.context.stroke();
    		}
	},
    // send the computed pictures to the server -> ML to count the number of fingers -> response
    sendPicture: function(){
            var msg = this.canvas.toDataURL('image/png').replace('data:image/png;base64,','');
            this.webSocket.send(JSON.stringify({
                'message': msg
            }));
    }
}

document.addEventListener("DOMContentLoaded", () => {

	const number = Math.floor(Math.random()*6);

	document.getElementById("goal").src = '/static/img/main'+number+'.png';

	draw.init();

	draw.initSocket(number);

});








