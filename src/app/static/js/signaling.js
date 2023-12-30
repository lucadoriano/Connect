let socket = new WebSocket("ws://localhost:9991");


socket.onopen = function(e) {
  console.log("Successfully connected to WebSocket")
};


socket.onmessage = function(event) {
  const connection = $("#connection-info").data()
  const data = JSON.parse(event.data);

  switch (data.type) {
    case "handshake":
      joinRoom(username=connection.current_user, room_id=connection.room)
      break;
    case "ready":
      $('#startCallLabel').html("Room - student is ready")
      $('#callModalStatus').html("You may now start the call.")
      $('#callButton').removeClass("disabled")
      break;
    case "offer":
      handleOffer(data);
      break;
    case "answer":
      handleAnswer(data);
      break;
    case "close":
      console.log(data)
      window.location.replace("/")
    case "log":
      console.log(data)
      break;
  }
};


socket.onclose = function(event) {
  if (event.wasClean) {
    console.log(`[close]: Connection closed, code=${event.code} reason=${event.reason}`);
  }
};


socket.onerror = function(error) {
  console.log(`[error]: ${error.message}`);
};


function sendToServer(message) {
  socket.send(JSON.stringify(message));
}


function joinRoom(username, room) {
  sendToServer({
    "type": "join", 
    "params": {
      "username": username,
      "room_id": room
    }
  });
}