const connection = document.getElementById('connection-info').dataset

const chatOutput = document.getElementById('chatOutput');
const localVideo = document.getElementById('localVideo');
const remoteVideo = document.getElementById('remoteVideo');

const toggleCamera = document.getElementById('camera-btn');
const toggleMic = document.getElementById('mic-btn');
const toggleShare = document.getElementById('share-btn');

let localStream;
let screenSharing = false;


const config = {
  iceServers: [{
    urls: "stun:stun.l.google.com:19302"
  }]
};


const mediaConstraints = {
  video: true,
  audio: true
}


const screenMediaConstraints = {
  video: {
    cursor: true
  },
  systemAudio: "exclude",
};


const peer = new RTCPeerConnection(config);
const dataChannel = peer.createDataChannel("chat", {
  negotiated: true,
  id: 0
});


navigator.mediaDevices.getUserMedia(mediaConstraints)
  .then(stream => {
    localStream = stream
    localVideo.srcObject = stream;
    localVideo.muted = true;

    stream.getTracks().forEach(track => peer.addTrack(track, stream));
  })
  .catch(error => console.error('Error accessing camera and/or microphone:', error));

peer.ontrack = (event) => {
  remoteVideo.srcObject = event.streams[0];
};

/* -------- CHAT - -------*/

const log = (msg, isSent) => {
  const messageClass = isSent ? 'msg-container right' : 'msg-container left';
  chatOutput.innerHTML += `<div class="${messageClass}"><div class="msg">${msg}</div></div>`;
};

dataChannel.onmessage = e => log(e.data, false); // Received message

chat.onkeypress = function(e) {
  if (e.keyCode != 13) return; // If not Enter key
  const message = chat.value;
  if (message.length > 0) {
    dataChannel.send(message);
    log(message, true); // Sent message
  }
  chat.value = ""; // Resets chat input after sending the message
};

/* ------------------------ */

async function createOffer() {
  await peer.setLocalDescription(peer.createOffer());
  peer.onicecandidate = ({
    candidate
  }) => {
    if (candidate) return;
    const offer = peer.localDescription.sdp;
    sendToServer({
      "type": "offer",
      "params": {
        "sender": connection.caller,
        "target": connection.callee,
        "sdp": JSON.stringify(offer)
      }
    })
  };
}


async function handleOffer(data) {
  if (peer.signalingState != "stable") return;
  console.log("You received an offer")

  await peer.setRemoteDescription({
    type: "offer",
    sdp: JSON.parse(data["sdp"])
  });
  
  await peer.setLocalDescription(await peer.createAnswer());
  peer.onicecandidate = ({
    candidate
  }) => {
    if (candidate) return;
    const answer = peer.localDescription.sdp;
    sendToServer({
      "type": "answer", 
      "params": {
        "sender": connection.callee,
        "target": connection.caller, 
        "sdp": JSON.stringify(answer) 
      }
    });
    console.log("Sent answer to caller")
  };
};


function handleAnswer(data) {
  if (peer.signalingState != "have-local-offer") return;
  peer.setRemoteDescription({
    type: "answer",
    sdp: JSON.parse(data["sdp"])
  });
};


async function shareScreen(){
  try {
    await navigator.mediaDevices.getDisplayMedia(screenMediaConstraints)
    .then(stream => {
      if (!screenSharing) {
        let videoTrack = stream.getVideoTracks()[0];
        let videoSender = peer.getSenders().find(sender => sender.track.kind === videoTrack.kind);

        localVideo.srcObject = stream;
        videoSender.replaceTrack(videoTrack);
        screenSharing = true;

        $('#share-btn').removeClass('btn-secondary')
        $('#share-btn').addClass('btn-danger')

        videoTrack.onended = function () {
          videoSender.replaceTrack(localStream.getTracks()[1]);
          localVideo.srcObject = localStream;
          screenSharing = false;

          $('#share-btn').removeClass('btn-danger')
          $('#share-btn').addClass('btn-secondary')
        }
      }
    });
  } catch (error) {
    console.error('Error:', error);
  }
}


function hangupCall() {
  peer.close()
  sendToServer({
    "type": "close",
    "params": {
      "room_id": connection.room
    }
  })
  window.location.replace("/")
  socket.close()
}


toggleCamera.addEventListener('click', () => {
  const videoTrack = localStream.getTracks().find(track => track.kind === 'video');
  if (videoTrack.enabled) {
    videoTrack.enabled = false;
    $('#camera-btn').removeClass('btn-secondary')
    $('#camera-btn').addClass('btn-danger')
  } else {
    videoTrack.enabled = true;
    $('#camera-btn').removeClass('btn-danger')
    $('#camera-btn').addClass('btn-secondary')
  } 
});


toggleMic.addEventListener('click', () => {
  const audioTrack = localStream.getTracks().find(track => track.kind === 'audio');
  if (audioTrack.enabled) {
    audioTrack.enabled = false;
    $('#mic-btn').removeClass('btn-secondary')
    $('#mic-btn').addClass('btn-danger')
  } else {
    audioTrack.enabled = true;
    $('#mic-btn').removeClass('btn-danger')
    $('#mic-btn').addClass('btn-secondary')
  }
});


toggleShare.addEventListener('click', (event) => {
  if (!screenSharing) {
    shareScreen();
  }
});


// Debug infos for connection state between peers
peer.onconnectionstatechange = ev => handleChange();
peer.oniceconnectionstatechange = ev => handleChange();

function handleChange() {
  console.log(`${new Date().toISOString()}: Connection state: ${peer.connectionState} - Ice Connection state: ${peer.iceConnectionState}`) 
}