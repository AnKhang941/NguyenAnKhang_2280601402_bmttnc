import tornado.ioloop
import tornado.websocket
import functools

class WebSocketClient:
    def __init__(self, io_loop):
        self.connection = None
        self.io_loop = io_loop

    def start(self):
        self.connect_and_read()

    def stop(self):
        self.io_loop.stop()

    def connect_and_read(self):
        print("Connecting to server...")
        future = tornado.websocket.websocket_connect(
            url="ws://localhost:8888/websocket/",
            on_message_callback=self.on_message,
            ping_interval=10,
            ping_timeout=30,
        )
        future.add_done_callback(self.maybe_retry_connection)

    def maybe_retry_connection(self, future):
        try:
            self.connection = future.result()
            print("Connected successfully!")
        except Exception as e:
            print(f"Could not connect: {e}. Retrying in 3 seconds...")
            self.io_loop.call_later(3, self.connect_and_read)

    def on_message(self, message):
        if message is None:
            print("Disconnected, reconnecting...")
            self.connect_and_read()
            return
        print(f"Received message from server: {message}")

def main():
    io_loop = tornado.ioloop.IOLoop.current()
    client = WebSocketClient(io_loop)
    io_loop.add_callback(client.start)
    io_loop.start()

if __name__ == "__main__":
    main()
