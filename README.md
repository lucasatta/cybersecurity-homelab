# Cybersecurity Homelab
A personal cybersecurity homelab focused on hands-on learning in **networking, Linux, network traffic analysis, and security fundamentals**.

This repository documents the configuration of my lab environment, the exercises I perform, the tools I use, and the concepts I learn along the way.

## Lab Architecture

The lab runs in **Oracle VirtualBox** and consists of two virtual machines:

- **Kali Linux** — analysis and testing machine
- **Ubuntu Server** — target machine

Both machines have a NAT adapter for Internet access and a second adapter connected to an isolated VirtualBox internal network named `cyberlab`.

```text
                 Oracle VirtualBox
┌───────────────────────────────────────────────┐
│                                               │
│   ┌────────────────┐  ┌───────────────────┐   │
│   │   Kali Linux   │  │   Ubuntu Server   │   │
│   │  10.10.10.10   │  │    10.10.10.20    │   │
│   │                │  │                   │   │
│   │ Analysis/Test  │  │      target       │   │
│   └───────┬────────┘  └────────┬──────────┘   │
│           │                    │              │
│           └─────────┬──────────┘              │
│                     │                         │
│         Internal network: cyberlab            │
│                                               │
└───────────────────────────────────────────────┘

```

## Lab Documentation

| Document | Description |
|---|---|
| [Network Setup](docs/network-setup.md) | VirtualBox network configuration, static IP addressing, and connectivity testing. |
| [Nmap Enumeration](docs/nmap-enumeration.md) | Basic port scanning, service identification, and version detection using Nmap. |
| [Wireshark Analysis](docs/wireshark-analysis.md) | Analysis of ICMP, HTTP, and TCP traffic, including the three-way handshake. |
| [SSH Log Analysis](docs/ssh-log-analysis.md) | Analysis of SSH authentication events and log filtering using Linux command-line tools. |

## Tools and Technologies

- **Virtualization:** Oracle VirtualBox
- **Operating systems:** Kali Linux, Ubuntu Server
- **Network analysis:** Nmap, Wireshark
- **Services:** SSH, Apache HTTP Server
- **Command-line tools:** `grep`, `awk`, `sort`, `uniq`, `journalctl`
- **Programming:** Python (basic scripting and automation)

## Learning Roadmap

### Completed

- [x] Set up a Kali Linux and Ubuntu Server homelab
- [x] Configure an isolated internal network
- [x] Test connectivity between virtual machines
- [x] Perform basic Nmap enumeration
- [x] Analyze ICMP, HTTP, and TCP traffic with Wireshark
- [x] Practice SSH authentication log analysis

### In Progress

- [ ] Document Python scripts for security-related tasks
- [ ] Expand Linux and network analysis exercises

### Planned

- [ ] Explore web security with Burp Suite
- [ ] Practice with intentionally vulnerable web applications
- [ ] Learn vulnerability assessment workflows
- [ ] Develop basic penetration testing and reporting skills

## Scope and Ethics

All exercises documented in this repository are performed in my own controlled lab environment or on systems where testing is explicitly authorized.

## Repository Purpose

This repository is both a practical learning journal and a way to document my progress in cybersecurity. Its content will evolve as I gain experience and complete new exercises.