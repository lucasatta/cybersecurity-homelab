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

## Authentication and Session Security

### Authentication Testing
The login endpoint was analyzed using Burp Suite Repeater:

`POST /rest/user/login HTTP/1.1`

Requests with valid and invalid credentials were compared.

| Test | HTTP Status | Result |
|---|---|---|
| Valid credentials | 200 OK | Authentication data and a token returned |
| Unregistered email | 401 Unauthorized | Generic error message |
| Registered account with incorrect password | 401 Unauthorized | Same generic error message |

Both unsuccessful login attempts returned the message:

`Invalid email or password.`

No user enumeration was observed through the HTTP status codes or error messages tested. This does not rule out other possible enumeration techniques.

### Session and Token Testing
After login, the authenticated endpoint `GET /rest/order-history` was examined by modifying the request headers in Burp Repeater.

| Request Headers | HTTP Status | Result |
|---|---|---|
| Valid Authorization and Cookie | 200 OK | Order history returned |
| Valid Authorization only, without Cookie | 200 OK | Order history returned |
| Cookie only, without Authorization | 500 Internal Server Error | Request failed |
| Invalid Authorization token | 500 Internal Server Error | Request failed |

For this endpoint, a valid Authorization token was sufficient to retrieve order history, while the Cookie header was not required in the tested requests.

Requests without a valid Authorization token did not return the protected order history. Instead, they produced `500 Internal Server Error` responses containing server-side error details, including internal file paths and stack traces.

This indicates potentially excessive error information disclosure. A controlled authentication or authorization error response without internal implementation details would be preferable.

> **Note:** These observations apply to the tested `/rest/order-history` endpoint and should not be generalized to every endpoint in the application.

## Authorization and Order Access Testing

### Test Setup
Two accounts were used to investigate access controls:

- **Account A:** One test order was created.
- **Account B:** A separate account with no orders.

Only accounts and order data created within the isolated lab were used.

### Order History Access
Both accounts requested:

`GET /rest/order-history HTTP/1.1`

| Authenticated Account | HTTP Status | Result |
|---|---|---|
| Account A | 200 OK | One order returned |
| Account B | 200 OK | Empty `data` array |

These results show that the order history endpoint returned different data according to the authenticated account in the tested scenario.

The order returned for Account A included an `orderId` and information such as email, total price and purchased products.

### Direct Order Tracking Access
The order identifier from Account A's order history matched the identifier used by the order tracking endpoint:

`GET /rest/track-order/<orderId> HTTP/1.1`

The same order tracking URL was tested with different authentication headers.

| Request Context | HTTP Status | Result |
|---|---|---|
| Original order tracking request | 200 OK | Account A's order details returned |
| Account B's Authorization and Cookie headers | 200 OK | Account A's order details returned |
| No Authorization or Cookie headers | 200 OK | Account A's order details returned |

The response included order-related information, including email, products and total price.

These tests demonstrate that the tracking endpoint returned the order details when the correct order identifier was provided, even without authentication.

### Security Assessment
This behavior raises a potential object-level access control concern, because a request associated with Account B, or with no authenticated session, could retrieve information about Account A's order.

However, some order tracking systems intentionally allow access through a hard-to-guess identifier that acts as an access secret. The observed behavior alone therefore does **not** conclusively establish an Insecure Direct Object Reference (IDOR) or Broken Object Level Authorization (BOLA) vulnerability.

The tests did not establish whether unauthenticated order tracking was intended, whether order identifiers could be guessed or enumerated, or whether an attacker could obtain identifiers belonging to other users.

A more complete assessment would require understanding the application's intended authorization model and the exposure of order identifiers.

## What I Learned
- How to intercept and inspect HTTP traffic using Burp Proxy and HTTP History;
- How to modify and resend HTTP requests using Burp Repeater;
- How to identify user-controlled parameters in API endpoints;
- How to analyze HTTP status codes, JSON responses and response lengths;
- How to compare server responses using Burp Comparer;
- How boolean conditions can help identify potential SQL Injection vulnerabilities;
- How to compare successful and unsuccessful authentication responses;
- How to test the role of Authorization and Cookie headers in authenticated requests;
- How invalid authentication can reveal excessive server-side error details;
- How to compare access to resources using separate test accounts;
- How to examine direct object references in API endpoints;
- Why observed access behavior must be distinguished from a confirmed IDOR vulnerability;
- Why security findings should be supported by reproducible evidence rather than a single unexpected response.