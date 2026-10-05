# Nmap Enumeration

## Objective
The objective of this lab is to start using tools such as Nmap for basic enumeration against a controlled Ubuntu Server target.

## Target
- Kali Linux: `10.10.10.10`
- Ubuntu Server: `10.10.10.20`
- Network: `cyberlab`

## Basic scan
```bash
nmap 10.10.10.20
```
This scan was used to identify open TCP ports on the Ubuntu Server target.

The scan showed that ports 22/tcp and 80/tcp were open.
## Service Version Detection
```bash
nmap -sV 10.10.10.20
```
This scan was used to detect the services running on the open ports and to gather version information.
## Observations
The basic scan identified two open TCP ports on the Ubuntu Server:

- `22/tcp` running SSH
- `80/tcp` running HTTP

The `-sV` scan provided additional information about the services and their versions.

Service version detection can help identify potentially outdated or vulnerable software, but a detected version alone is not enough to confirm that a vulnerability is actually present.
## What I Learned

- What enumeration is;
- The role of Nmap in network enumeration and security assessment;
- What a vulnerability is and why keeping software up to date is important;
- Why service and version detection does not automatically prove that a system is vulnearble.
- The differences between open, closed, and filtered ports.