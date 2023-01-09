// const video = document.getElementById("video-input")
const video = document.createElement("video")
const captureVideoButton = document.querySelector(".capture-button")
const stopVideoButton = document.querySelector(".stop-button")
const socket = io('http://103.161.112.166:9980');



socket.on("connect", () => {
	console.log("connect: ")
});

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

			// 
			// SendDataSet()

		})
		.catch((err) => {
			console.log(err);
		});
};

function StopVideo() {
	stream_status = false
	localStream.getVideoTracks()[0].stop();
	video.src = "";
}

stopVideoButton.onclick = StopVideo


async function GetFaceId(body) {
	var response = await fetch('/api/face-id', {
		method: 'POST',
		headers: {
			'Accept': 'application/json',
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(body)
	})
	return response.json()
}

async function PostDataSet(body) {
	var response = await fetch('/api/dataset', {
		method: 'POST',
		headers: {
			'Accept': 'application/json',
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(body)
	})
	return response.json()
}



var count = 0
var step = 0
var mode = 0
var face_id = 0
var user_id = 0
video.addEventListener('loadeddata', SendDataSet)
function SendDataSet() {
	if (stream_status) {
		const video_output = document.getElementById('video-output')
		const canvas = document.createElement('canvas')
		const ctx = canvas.getContext('2d')
		ctx.drawImage(video, 0, 0, canvas.width, canvas.height)

		if (step == 0) {
			GetFaceId({ image_base64: canvas.toDataURL() }).then((data) => {
				video_output.src = data.img
				if (data.id != 0) {
					face_id = data.id
					StopVideo()
					step = 2
				}
				else if (count >= 50) {

					step = 1
				} else {
					count++
				}
				SendDataSet()
			})
		} else if (step == 1) {
			console.log("time over")
			PostDataSet({
				id: user_id,
				image_base64: canvas.toDataURL()
			}).then((data) => {
				user_id = data.user_id
				video_output.src = data.img
				if (data.id != 0) {
					face_id = data.id
					StopVideo()
					step = 2

				}
				SendDataSet()
			})
		}
	} else {
		if (step == 2) {
			console.log("Step 2")
			socket.emit("hoangxuannam/car_control", true)
			processVideo('')
		}
	}
}


function processVideo(src) {
	const video_output = document.getElementById('video-output')
	const fetchOptions = {
		method: "GET",
		headers: {
			"Content-Type": "application/json",
			"Accept": "application/json"
		}
	};
	fetch('/api/car', fetchOptions)
		.then((response) => response.json())
		.then((data) => {
			// console.log(data)
			// ShowTelemetry(data.telemetry)
			processVideo(data)
			// return data;
		});
	if (src != null) {
		video_output.src = src
	}

}