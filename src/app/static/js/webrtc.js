const output = document.getElementById('output');
const toggleCamera = document.getElementById('camera-btn');
const toggleMic = document.getElementById('mic-btn');
const toggleShare = document.getElementById('share-btn');
const connection = document.getElementById('connection-info').dataset

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
const dc = peer.createDataChannel("chat", {
  negotiated: true,
  id: 0
});

navigator.mediaDevices.getUserMedia(mediaConstraints)
  .then(stream => {
    localStream = stream
    const localVideo = document.getElementById('localVideo');
    localVideo.srcObject = stream;
    localVideo.muted = true;

    stream.getTracks().forEach(track => peer.addTrack(track, stream));
  })
  .catch(err => console.error('Error accessing camera and/or microphone:', err));

peer.ontrack = (event) => {
    const remoteVideo = document.getElementById('remoteVideo');
    remoteVideo.srcObject = event.streams[0];
};

const log = (msg, isSent) => {
  const messageClass = isSent ? 'msg-container right' : 'msg-container left';
  output.innerHTML += `<div class="${messageClass}"><div class="msg">${msg}</div></div>`;
};

dc.onopen = () => chat.select();
dc.onmessage = e => log(e.data, false); // Received message
peer.oniceconnectionstatechange = e => log(peer.iceConnectionState, true); // Sent message

chat.onkeypress = function(e) {
  if (e.keyCode != 13) return;
  const message = chat.value;
  dc.send(message);
  log(message, true); // Sent message
  chat.value = "";
};


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
  console.log(`you received the offer`)

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
    console.log(answer)
  };
};

function setAnswer(data) {
  if (peer.signalingState != "have-local-offer") return;
  peer.setRemoteDescription({
    type: "answer",
    sdp: JSON.parse(data["sdp"])
  });
};

peer.onconnectionstatechange = ev => handleChange();
peer.oniceconnectionstatechange = ev => handleChange();

function handleChange() {
  let stat = 'ConnectionState: <strong>' + peer.connectionState + '</strong> IceConnectionState: <strong>' + peer.iceConnectionState + '</strong>';
  document.getElementById('stat').innerHTML = stat;
  console.log('%c' + new Date().toISOString() + ': ConnectionState: %c' + peer.connectionState + ' %cIceConnectionState: %c' + peer.iceConnectionState,
    'color:black', 'color:red', 'color:black', 'color:red');
}
handleChange();

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


async function shareScreen(){
  try {
    await navigator.mediaDevices.getDisplayMedia(screenMediaConstraints)
    .then(stream => {
      if (!screenSharing) {
        let videoTrack = stream.getVideoTracks()[0];
        let videoSender = peer.getSenders().find(sender => sender.track.kind === videoTrack.kind);
        const localVideo = document.getElementById('localVideo');
        localVideo.srcObject = stream;
        screenSharing = true;
        $('#share-btn').removeClass('btn-secondary')
        $('#share-btn').addClass('btn-danger')

        videoSender.replaceTrack(videoTrack);

        videoTrack.onended = function(){
          videoSender.replaceTrack(localStream.getTracks()[1]);
          localVideo.srcObject = localStream;
          screenSharing = false;
          $('#share-btn').removeClass('btn-danger')
          $('#share-btn').addClass('btn-secondary')
        }
      }
    });
  } catch (err) {
    console.error('Error:', err);
  }
}


toggleShare.addEventListener('click', (event) => {
  if (!screenSharing) {
    shareScreen();
  }
});