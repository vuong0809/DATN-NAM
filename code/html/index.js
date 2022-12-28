// const video = document.getElementById("video-input")
const video = document.createElement("video")
const captureVideoButton = document.querySelector(".capture-button")
const stopVideoButton = document.querySelector(".stop-button")


var stream_status = false
captureVideoButton.onclick = function () {
	navigator.mediaDevices
		.getUserMedia({
			// audio: false,
			video: true
			// video: {
			// 	width: { exact: 720 },
			// 	height: { exact: 576 }
			// }
		})
		.then((stream) => {
			window.localStream = stream;
			video.srcObject = stream;
			video.play()

			// audio.srcObject = stream;
			stream_status = true

			// video.addEventListener('loadeddata', SendDataSet)
			// SendDataSet()

		})
		.catch((err) => {
			console.log(err);
		});
};

stopVideoButton.onclick = function () {
	stream_status = false

	localStream.getVideoTracks()[0].stop();
	video.src = "";

	// localStream.getAudioTracks()[0].stop();
	// audio.src = "";
};


setInterval(SendDataSet, (1 / 1000))

function SendDataSet() {
	if (stream_status) {
		const video_output = document.getElementById('video-output')
		const canvas = document.createElement('canvas')
		const ctx = canvas.getContext('2d')
		ctx.drawImage(video, 0, 0, canvas.width, canvas.height)
		var img_b64 = canvas.toDataURL()
		img_b64 = img_b64.split(',')[1]
		


		video_output.src = `data:image/png;base64,${img_b64}`
		// SendDataSet()
	}
}