#!/bin/bash
# Example commands for the network scavenger hunt. Replace 192.168.10.0/24 and IPs with your subnet.

# Host discovery (no port scan)
nmap -sn 192.168.10.0/24

# After ping sweep, show ARP table
arp -a
# or
ip neigh show

# Fast port scan on one host
nmap -F 192.168.10.11

# Specific ports, with service detection
nmap -sV -p 22,80,443 192.168.10.11

# What's listening on this machine
ss -tlnp
