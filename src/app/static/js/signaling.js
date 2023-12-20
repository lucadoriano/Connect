let socket = new WebSocket("ws://localhost:9991");

socket.onopen = function(e) {
  console.log("Successfully connected to WebSocket")
};

socket.onmessage = function(event) {
  console.log(`[server] ${event.data}`);
  const data = JSON.parse(event.data);

  if (data.type === 'offer') {
    handleOffer(data);
  } else if (data.type === 'answer') {
    console.log("i received an answer")
    setAnswer(data);
  }
};

socket.onclose = function(event) {
  if (event.wasClean) {
    alert(`[close] Connection closed, code=${event.code} reason=${event.reason}`);
    socket.send("")
  } else {

  }
};

socket.onerror = function(error) {
  alert(`[error] ${error.message}`);
};

function sendToServer(message) {
  socket.send(JSON.stringify(message));
}

function get_rooms() {
  sendToServer({
    "type": "list_rooms", 
    "params": {}
  });
}


function clients() {
  socket.send(JSON.stringify({
    "type": "clients",
    "params": {

    }
  }));
}

function closea() {
  socket.close()
}

function join(username, room) {
  sendToServer({
    "type": "join", 
    "params": {
      "username": username,
      "room_id": room
    }
  });
}

