import socket
import struct

MSG_LENGTH_BYTES = 4

class ConnectionClosed(Exception): pass

def send_message(socket, message):
    msg_length = len(message)
    network_order_unsigned_int = "!I"
    socket.sendall(struct.pack(network_order_unsigned_int, msg_length))
    socket.sendall(message)

def receive_message(socket):
    num_size_bytes_recvd = 0
    msg_size_buffer = b''
    while num_size_bytes_recvd < MSG_LENGTH_BYTES:
        msg_size_chunk = socket.recv(MSG_LENGTH_BYTES - num_size_bytes_recvd)
        if not msg_size_chunk:
            socket.close()
            raise ConnectionClosed
        msg_size_buffer += msg_size_chunk
        num_size_bytes_recvd += len(msg_size_chunk)

    msg_size = int.from_bytes(msg_size_buffer, "big")
    num_msg_bytes_recvd = 0
    msg_buffer = b''
    while num_msg_bytes_recvd < msg_size:
        msg_chunk = socket.recv(msg_size - num_msg_bytes_recvd)
        if not msg_chunk:
            socket.close()
            raise ConnectionClosed
        msg_buffer += msg_chunk
        num_msg_bytes_recvd += len(msg_chunk)

    return msg_buffer
