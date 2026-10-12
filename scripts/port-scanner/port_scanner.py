import socket

target = "10.10.10.20"

start_port = 20
end_port = 100

print(f"Scanning {target}...")

for port in range (start_port, end_port + 1):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)

    try:
        result = sock.connect_ex((target, port))

        if result == 0:
            print(f"[OPEN] Port {port}")
            
    except OSError as error:
        print(f"[ERROR] Port {port}: {error}")
        
    finally:
        sock.close()

print("Scan completed")