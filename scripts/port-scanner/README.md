# TCP Port Scanner

A simple TCP port scanner written in Python as part of my cybersecurity learning journey.

## Objective

Practice basic Python socket programming and understand how TCP connections can be used to identify open ports.

## How It Works

The script:

1. Defines a target IPv4 address and a range of ports.
2. Creates a TCP socket for each port.
3. Attempts to establish a connection using `connect_ex()`.
4. Prints the ports that accept a TCP connection.
5. Closes each socket after the connection attempt.

## Configuration

The target and port range are currently defined directly in the script:

- Target: `10.10.10.20` (Ubuntu Server in my homelab)
- Port range: `20–100`
- Connection timeout: `0.5` seconds

## Usage

Run the script with Python:

`python port_scanner.py`

## Limitations

- The scanner is sequential and may be slow for large port ranges.
- It performs TCP connection attempts, not SYN scanning.
- A failed connection does not necessarily mean a port is closed.
- The target and port range are currently hardcoded.

## Planned Improvements

- Add command-line arguments using `argparse`.
- Validate target addresses and port ranges.
- Improve error handling and result reporting.

## Ethical Use

This script is intended for educational use on systems I own or have explicit permission to test.