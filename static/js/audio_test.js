let audioCounter = { 
     recordAudio : async function(){
        return new Promise(async resolve => {
          this.stream = await navigator.mediaDevices.getUserMedia({ audio: true });
          this.mediaRecorder = new MediaRecorder(this.stream);
          this.audioChunks = [];
          this.mediaRecorder.addEventListener('dataavailable', event => {
            this.audioChunks.push(event.data);
          });
          var recordAudioStart = function(){
            this.audioChunks = [];
            this.mediaRecorder.start();
          };
          var recordAudioStop = function(){
            new Promise(resolve => {
              this.mediaRecorder.addEventListener('stop', () => {
                const audioBlob = new Blob(this.audioChunks);
                const audioUrl = URL.createObjectURL(audioBlob);
                this.audio = new Audio(audioUrl);
                const play = () => this.audio.play();
		var ac = this.audioChunks;
                resolve({ ac, audioBlob, audioUrl, play });
              });
              this.mediaRecorder.stop();
            })};
          resolve({ recordAudioStart, recordAudioStop });
      })},
      bordel :function(){
      const sleep = time => new Promise(resolve => setTimeout(resolve, time));
      this.recordButton = document.getElementById('record');
      this.stopButton = document.getElementById('stop');
      this.playButton = document.getElementById('play');
      this.saveButton = document.getElementById('save');
      this.recorderSaved = false;
      this.savedAudioMessagesContainer = document.querySelector('#saved-audio-messages');
      const ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
      const webSocket = new WebSocket(ws_scheme+ '://' + window.location.host +'/ws/audio/');
      let recorder;
      let audio;
      this.recordButton.addEventListener('click', async () => {
        document.getElementById("record").disabled = true;
        document.getElementById("stop").disabled = false;
        document.getElementById("play").disabled = true;
        document.getElementById("save").disabled = true;
        if (!this.recorderSaved) {
          this.recorderSaved = true;
          this.recorder = await this.recordAudio();
        }
        this.recorder.start();
      });
      this.stopButton.addEventListener('click', async () => {
        document.getElementById("record").disabled = false;
        document.getElementById("stop").disabled = true;
        document.getElementById("play").disabled = false;
        document.getElementById("save").disabled = false;
        audio = await this.recorder.stop();
      });
      this.playButton.addEventListener('click', () => {
        audio.play();
      });
      this.saveButton.addEventListener('click', () => {
        const reader = new FileReader();
        reader.readAsDataURL(audio.audioBlob);
        reader.onload = () => {
          const base64AudioMessage = reader.result.split(',')[1];
          webSocket.send(JSON.stringify({
                'message': base64AudioMessage
            }));
          };
        });
}
};
      
document.addEventListener("DOMContentLoaded", () => {

      var number = Math.floor(Math.random()*6);

      audioCounter.bordel();
      
});



