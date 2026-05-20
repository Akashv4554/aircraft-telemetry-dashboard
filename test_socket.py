import socketio

sio = socketio.Client()


@sio.event
def connect():
    print("Connected to server")


@sio.event
def disconnect():
    print("Disconnected from server")


@sio.on("telemetry_update")
def telemetry_update(data):
    print("Telemetry Update:")
    print(data)


sio.connect("http://127.0.0.1:5000")

sio.wait()