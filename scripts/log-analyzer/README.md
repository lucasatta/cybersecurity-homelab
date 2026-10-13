# Login Log Analyzer

A simple Python log analyzer developed as part of my cybersecurity learning journey.

## Overview

This script analyzes a simplified authentication log format to identify repeated failed login attempts from the same IP address.

The project was created to practice Python file handling, dictionaries, functions, exception handling, and command-line arguments while exploring basic security monitoring concepts.

## Features

- Reads authentication events from a text file.
- Ignores empty lines and incorrectly formatted entries.
- Counts `LOGIN_FAILED` events for each IP address.
- Generates an alert when the number of failed attempts reaches a configurable threshold.
- Handles missing log files.

## Expected Log Format

Each line contains three space-separated fields:

`IP_ADDRESS EVENT USERNAME`

Example:

```text
192.168.1.10 LOGIN_FAILED admin
192.168.1.10 LOGIN_FAILED admin
192.168.1.20 LOGIN_SUCCESS luca
192.168.1.10 LOGIN_FAILED root
192.168.1.30 LOGIN_FAILED guest
```

Only `LOGIN_FAILED` events are counted.

## Usage

Run the script with Python:

```bash
python log_analyzer.py sample.log
```

Set a custom alert threshold:

```bash
python log_analyzer.py sample.log --threshold 5
```

The default threshold is `3`.

## Example Output

```text
192.168.1.10 -> 3 login falliti -> ALERT
192.168.1.30 -> 1 login fallito
```

## Limitations

- The script expects a simplified, three-field log format rather than raw Linux authentication logs.
- It does not validate IP addresses or usernames.
- It does not correlate events over time.
- It does not detect attacks automatically; alerts are based only on the configured number of failed attempts.

## Future Improvements

- Support real OpenSSH authentication logs.
- Validate input data.
- Add timestamp analysis.
- Export results to CSV or JSON.

## Ethical Use

This project is intended for educational purposes and analysis of logs from authorized systems.