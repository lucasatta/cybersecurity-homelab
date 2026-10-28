# Web Application Security Testing with Burp Suite

## Objective
The objective of this lab is to analyze HTTP communication, manipulate web requests and identify potential web application vulnerabilities using Burp Suite Community Edition and OWASP Juice Shop.

The testing was performed in an isolated homelab environment against an intentionally vulnerable web application.

## Lab Environment
The laboratory consists of two virtual machines:

| Machine | IP Address | Purpose |
|---|---|---|
| Kali Linux | 10.10.10.10 | Security testing |
| Ubuntu Server | 10.10.10.20 | Web application hosting |

OWASP Juice Shop was deployed on Ubuntu Server using Docker and accessed from Kali Linux at:

`http://10.10.10.20:3000`

The main tools used were:

- Burp Suite Proxy
- Burp Suite HTTP History
- Burp Suite Repeater
- Burp Suite Comparer
- OWASP Juice Shop
- Docker

## HTTP Traffic Analysis
Burp Suite's embedded browser was used to access OWASP Juice Shop and inspect the HTTP communication between the browser and the application.

HTTP requests were analyzed using Proxy > HTTP History.

The initial request was:

`GET / HTTP/1.1`

The server responded with `200 OK`.

The request was then sent to Burp Repeater, where the requested path was modified:

`GET /percorso-inesistente-test HTTP/1.1`

Both requests returned `200 OK`.

This behavior is consistent with a Single Page Application (SPA), where the server may return the frontend HTML document even when an unknown path is requested.

However, the response status alone is not sufficient to confirm that both requests returned identical content.

## API Endpoint Analysis
The following endpoint was tested using Burp Repeater:

`GET /rest/products/search?q=apple HTTP/1.1`

The server returned `200 OK` with a JSON response containing product information.

Changing the `q` parameter from `apple` to `banana` changed the products returned by the application.

This confirmed that the `q` parameter influences the search results and could be investigated further as a user-controlled input.

## Input Validation Testing
Different values were submitted through the `q` parameter to observe how the application handled user input.

The following tests were performed:

| Input | HTTP Status | Result |
|---|---|---|
| `apple` | 200 OK | Matching products |
| Empty parameter | 200 OK | Product list |
| `'` | 200 OK | Empty results |
| `xyznonexistent123` | 200 OK | Empty results |

The apostrophe was submitted using its URL-encoded representation, `%27`.

Both the apostrophe and the nonexistent search term returned an empty `data` array.

This behavior did not provide sufficient evidence of SQL Injection, so additional testing was performed.

## SQL Injection Testing
The `q` parameter was tested with SQL expressions designed to evaluate whether user input could influence the application's database query.

The initial payloads were:

`')) OR 1=1--`

`')) OR 1=2--`

Both returned product lists, without a meaningful difference in the application data.

Additional tests were performed using `AND` conditions:

**True condition:**

`')) AND 1=1--`

**False condition:**

`')) AND 1=2--`

The results were:

| Condition | HTTP Status | Result |
|---|---|---|
| `AND 1=1` | 200 OK | Product list |
| `AND 1=2` | 200 OK | Empty results |

The two responses were compared using Burp Comparer.

The true condition returned a JSON response containing products, while the false condition returned:

`{"status":"success","data":[]}`

The different responses to logically true and false conditions provide strong evidence that the input is influencing the SQL query.

> **Note:** The observed behavior is strongly indicative of SQL Injection in the intentionally vulnerable application. The tests did not include database data extraction or an assessment of the full potential impact.

## Security Considerations
SQL Injection vulnerabilities may occur when an application incorporates untrusted user input into SQL queries without properly separating data from executable SQL syntax.

Depending on the database permissions and application architecture, successful exploitation may lead to unauthorized access to information or other database operations.

A primary mitigation is to use parameterized queries or prepared statements instead of constructing SQL queries through string concatenation.

## What I Learned
- How to intercept and inspect HTTP traffic using Burp Proxy and HTTP History;
- How to modify and resend HTTP requests using Burp Repeater;
- How to identify user-controlled parameters in API endpoints;
- How to analyze HTTP status codes, JSON responses and response lengths;
- How to compare server responses using Burp Comparer;
- How boolean conditions can help identify potential SQL Injection vulnerabilities;
- Why security findings should be supported by reproducible evidence rather than a single unexpected response.