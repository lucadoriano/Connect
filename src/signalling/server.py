import socket
import json

from websocket.websocket import WebSocket



MAX_USERS = 2

rooms = {}
clients = {}


def send_to_room(roomid, message):
    if rooms[roomid]:
        for user in rooms[roomid]:
            ws.send(get_user_client(user), json.dumps(message))

def send_log(client, message):
    ws.send(client, json.dumps({
        "type": "log",
        "message": message
    }))

def get_user_client(user):
    for username, client in clients.items():
        if user == username:
            return client


def get_client_username(socket):
    for username, client in clients.items():
        if client == socket:
            return username

def remove_from_room(username):
    for room_id, users in rooms.items():
        if username in users:
            index = rooms[room_id].index(username)
            rooms[room_id].pop(index)

def remove_empty_room():
    rooms_to_remove = []
    for room_id, users in rooms.items():
        if not users:
            rooms_to_remove.append(room_id)

    for room_id in rooms_to_remove:
        rooms.pop(room_id, None)


def send_to_user(username, message):
    client = get_user_client(username)
    ws.send(client, json.dumps(message))

def onmessage(client: socket.socket, message: str):
    # print(f"Message from {client.getpeername()}: {message}")
    try:
        type, params = json.loads(message).values()
        
        if type == "join":
            username = params["username"]
            room_id  = params["room_id"]

            if not room_id in rooms.keys():
                if room_id:
                    rooms[room_id] = []
                    send_log(client, "Room does not exist, created now") 
                else:
                    send_log(client, "Room ID is undefined")

            if len(rooms[room_id]) >= MAX_USERS:
                send_log(client, "Room is full")
                send_log(client, rooms[room_id])
            #     return

            if username not in rooms[room_id]:
                rooms[room_id].append(username)
                clients[username] = client
                send_log(client, f"{username} joined room {room_id}")

                if len(rooms[room_id]) >= MAX_USERS:
                    send_to_room(room_id, {
                        "type": "ready",
                        "callee": f"{username}",
                        "status": "All users have joined"
                    })
            else:
                send_log(client, "User already in room")
   
        if type == "offer":
            sender = params["sender"]
            target = params["target"]
            sdp = params["sdp"]

            send_to_user(target, {"type": "offer", "sender": sender, "sdp": sdp})

        if type == "answer": 
            sender = params["sender"]
            target = params["target"]
            sdp = params["sdp"]

            send_to_user(target, {"type": "answer", "sender": sender, "sdp": sdp})
            
        if type == "close":
            room_id = params["room_id"]
            send_to_room(room_id, {
                "type": "close",
                "status": "Call has been ended"
            })
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")




def onopen(client: socket.socket):
    print(f"Client connected: {client.getpeername()}")


def onclose(client: socket.socket):
    username = get_client_username(client)
    remove_from_room(username=username)
    remove_empty_room()
    print(f"Client [{username}] disconnected - {client.getpeername()}")

    
if __name__ == '__main__':
    ws = WebSocket("localhost", 9991)
    ws.onmessage(onmessage)
    ws.onopen(onopen)
    ws.onclose(onclose)
    ws.start()