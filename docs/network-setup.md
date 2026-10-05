# Network Setup

## Objective
The objective of this lab is to create a controlled environment for practicing basic networking and cybersecurity concepts.

## Lab Environment
The lab consists of two virtual machines running in Oracle VirtualBox:
- Kali Linux, used as the analysis/testing machine
- Ubuntu Server, used as the target/server machine

## Network Configuration
Both virtual machines use a NAT interface for Internet access and a second interface connected to the VirtualBox internal network 'cyberlab'.

- Kali Linux: `10.10.10.10/24`
- Ubuntu Server: `10.10.10.20/24`

No default gateway is configured on the internal network interface, since communication between the two virtual machines happens within the same subnet.

## Connectivity Test
Connectivity between the two virtual machines was verified using 'ping' from Kali Linux to ubuntu Server and vice versa.

## What I Learned
- The difference between NAT and an internal network;
- How two hosts can communicate directly within the same subnet;
- What a default gateway is and why the internal interfaces do not need one;
- The difference between public and private IP addresses, and between static and dynamic addressing;
- What ICMP is and how to verify connectivity using ping.