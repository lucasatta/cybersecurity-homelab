# SSH Log Analysis

## Objective
The objective of this lab is to analyze SSH authentication events on Ubuntu Server and practice basic log analysis using Linux command-line tools.

## Log Source
The analysis was performed using the Ubuntu authentication log:

`/var/log/auth.log`

The main tools used were:

- `grep`
- `awk`
- `sort`
- `uniq`
- `wc`
- `journalctl`

## Failed Login Analysis
Failed SSH authentication attempts were generated from Kali Linux against the Ubuntu Server.
To identify failed password authentication events, I filtered the authentication log using:
`sudo grep "Failed password" /var/log/auth.log`

I then filtered the events for a specific user and extracted the source IP address:
`sudo grep "Failed password for luca" /var/log/auth.log | awk '{print $9}'`

To count failed login attempts by source IP:
`sudo grep "Failed password for luca" /var/log/auth.log | awk '{print $9}' | sort | uniq -c | sort -nr`

The pipeline filters failed authentication events, extracts the source IP address, groups identical addresses, counts their occurrences and sort the results by frequency

> **Note:** The `awk '{print $9}'` command relies on the log format observed in this lab. Different SSH log entries may have different field structure, so the position of the source IP should always be verified.

## Successful login Analysis
Successful SSH authentication events were identified by searching for `Accepted` entries in the authentication log:
`sudo grep "Accepted" /var/log/auth.log`

These entries can provide useful information such as the authenticated user, source IP address, authenticated method and connection details.

Comparing successful and failed authentication events helps distinguish normal access from potentially suspicious login activity.

## Timeline Correlation
Authentication events were reviewed together with their timestamps to understand the sequence of SSH activity.

For example, multiple failed authentication attempts followes by a succesful login can be more significant than an isolated failed attempt.

The timestamp, username, source IP address and authentication result can therefore be correlated to reconstruct the sequence of events and provide additional context during an investigation.

## What I Learned
- How SSH authentication events are recorded in Linux logs;
- How to identify successful and failed SSH login attempts;
- How to filter log entries using command-line tools such ad `grep`, `awk`, `sort` and `uniq`;
- How to count authentication attempts by source IP address;
- How timestamps and multiple log events can be correlated to reconstruct authentication activity.