
""" 
  ┌────────────────────────────────────────────────────────────────────────────┐
  └                     Connect to Chroma Over Ethernet                        ┘
  ┌────────────────────────────────────────────────────────────────────────────┐
  │ The short script is a example that open a socket, sends a query,           │
  | print the return message and closes the socket.                            │
  │============================================================================|
  | Initialize instrument IP and Port at the top as globals, in 'if __name__'  |
  │ block at the bottom, or in any of the function calls using these params    |
  └────────────────────────────────────────────────────────────────────────────┘
"""

import socket
import sys
import time

# —————————————————————————–
# Chroma IP & port here
# —————————————————————————–
INSTRUMENT_IP:str = "192.168.0.17"
INSTRUMENT_PORT:int = 5024  # the port number of the instrument service
BUFFER_SIZE:int = 4096


def get_socket(instrument_ip:str, instrument_port:int, buffer_size:int) -> socket.socket:
    """get_socket get instrument socket using provided ip, port and buffer size

    prints error and quits immediately if socket error
    prints initial socket buffer content if success

    Parameters
    ----------
    instrument_ip : str
        IP address of instrument
    instrument_port : int
        port of instrument
    buffer_size : int
        length of buffer (bytes) to read

    Returns
    -------
    socket.socket
        instrument socket indicated by passed arguments
    """

    try:
        # create an AF_INET, STREAM socket (TCP)
        s:socket.socket = socket.socket(socket.AF_INET, socket.sock_STREAM)

    except socket.error:
        print("Failed to create socket.")
        sys.exit()

    try:
        # Connect to remote server
        s.connect(
            (
                instrument_ip, 
                instrument_port
            )
        )
        info = s.recv(buffer_size)

        print(info)

    except socket.error:
        print("failed to connect to ip " + INSTRUMENT_IP)

    return s


def query_socket(inst:socket.socket, scpi_command:str) -> bytes:
    """query_socket queries socket provided using SCPI command provided

    NOTE: the return type is `bytes`

    Parameters
    ----------
    inst : socket.socket
        your instrument socket
    scpi_command : str
        command to send to instrument

    Returns
    -------
    bytes
        response from instrument

    Print error and exit immediately if socket error
    """
    try:
        # Send scpi_command string
        inst.sendall(scpi_command)
        time.sleep(1)
    except socket.error:
        # Send failed
        print("Send failed")
        sys.exit()
    response: bytes = inst.recv(4096)
    return response


def socketClose(inst:socket.socket):
    inst.close()
    time.sleep(0.5)


def main(instrument_ip:str, instrument_port:int, buffer_size:int, scpi_command:bytes):
    """main initializes socket using ip, port and buffer size

    main goes on to query instrument 10 times using SCPI `scpi_command`

    Parameters
    ----------
    instrument_ip : str
        IP address of instrument
    instrument_port : int
        port of instrument
    buffer_size : int
        length of buffer (bytes) to read
    """

    instrument_socket_instance:socket = get_socket(
        instrument_ip=instrument_ip, 
        instrument_port=instrument_port, 
        buffer_size=buffer_size
    )

    # —————————————————————————–————————————————
    # NOTE: scpi_command is not string; it's bytes
    # NOTE: same is true of instrument_response
    # —————————————————————————————————————————–
    
    for count, _ in enumerate(range(10)):
        instrument_response:bytes = query_socket(
            inst=instrument_socket_instance, 
            scpi_command=scpi_command
        )
        print(f'{count+1} :: {str(instrument_response)}')

    socketClose(instrument_socket_instance)

    input('Press "Enter" to exit')


if __name__ == "__main__":

    # —————————————————————————–——————————
    # You can set these here or at the top
    # ———————————————————————————————————–
    instrument_ip = INSTRUMENT_IP
    instrument_port = INSTRUMENT_PORT
    buffer_size = BUFFER_SIZE

    scpi_command:bytes = b"*IDN?"

    main(
        instrument_ip=instrument_ip, 
        instrument_port=instrument_port, 
        buffer_size=buffer_size,
        scpi_command=scpi_command
    )
