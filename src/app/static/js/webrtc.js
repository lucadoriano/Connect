const output = document.getElementById('output');

const config = {
  iceServers: [{
    urls: "stun:stun.l.google.com:19302" // list of free STUN servers: https://gist.github.com/zziuni/3741933
  }]
};

const mediaConstraints = {
    video: true,
    audio: true
}

const peer = new RTCPeerConnection(config);
const dc = peer.createDataChannel("chat", {
  negotiated: true,
  id: 0
});

navigator.mediaDevices.getUserMedia(mediaConstraints)
  .then(stream => {
    const localVideo = document.createElement('video');
    localVideo.srcObject = stream;
    localVideo.autoplay = true;
    localVideo.muted = true;
    videoContainer.appendChild(localVideo);

    stream.getTracks().forEach(track => peer.addTrack(track, stream));
  })
  .catch(err => console.error('Error accessing camera and/or microphone:', err));

peer.ontrack = (event) => {
  const remoteVideo = document.getElementById('remoteVideo');
  if (!remoteVideo) {
    const newRemoteVideo = document.createElement('video');
    newRemoteVideo.id = 'remoteVideo';
    newRemoteVideo.srcObject = event.streams[0];
    newRemoteVideo.autoplay = true;
    videoContainer.appendChild(newRemoteVideo);
  }
};

const log = msg => output.innerHTML += `<br>${msg}`;
dc.onopen = () => chat.select();
dc.onmessage = e => log(`> ${e.data}`);
peer.oniceconnectionstatechange = e => log(peer.iceConnectionState);

chat.onkeypress = function(e) {
  if (e.keyCode != 13) return;
  dc.send(chat.value);
  log(chat.value);
  chat.value = "";
};

async function createOffer() {
  const connection = $("#connection-info").data()
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
  const connection = $("#connection-info").data()
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