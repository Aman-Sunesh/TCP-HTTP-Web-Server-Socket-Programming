# TCP / HTTP Web Server — Socket Programming (Python)

A minimal HTTP server implemented with raw TCP sockets in Python. This project demonstrates how HTTP requests are received and parsed over TCP, how files are served from a local directory, and how standard HTTP response headers (including cookies) are constructed and returned.

---

## Repository Structure

```
TCP-HTTP-Web-Server-Socket-Programming/
├── html_files/                     # Static assets served by the server
│   └── index.html                  # Example HTML page
├── tcp_http_web_server.py          # Main TCP/HTTP server
└── README.md                       # Project overview (this file)
```

---

## Features

- Pure-Python TCP socket server (no external web frameworks)
- Serves a static HTML page from `html_files/`
- Sends a well-formed `HTTP/1.1 200 OK` response with common headers
- Demonstrates cookie setting via `Set-Cookie: coursename=CompNet`
- Returns a minimal `404 Not Found` HTML body when the page is missing

> **Note:** This project is intentionally simple for educational purposes. See **Known Limitations** below.

---

## Prerequisites

- Python 3.8+ (tested on 3.10/3.11)
- A terminal (PowerShell on Windows, or any shell on macOS/Linux)

---

## Installation

### 1) Clone or Download
```bash
git clone https://github.com/Aman-Sunesh/TCP-HTTP-Web-Server-Socket-Programming.git
cd TCP-HTTP-Web-Server-Socket-Programming
```

(Or download the repository as a ZIP and extract it.)

### 2) Verify Files
You should see:
- `tcp_http_web_server.py`
- `html_files/index.html`

---

## Running the Server

### Windows (PowerShell)
```powershell
python .	cp_http_web_server.py
```

### macOS / Linux
```bash
python3 tcp_http_web_server.py
```

If successful, you'll see:
```
The server is ready to receive
```

Now open a browser and visit:
```
http://127.0.0.1:12345/
```
You should see the test page from `html_files/index.html`.

---

## Quick Test with cURL

```bash
curl -i http://127.0.0.1:12345/
```

Example response (headers will vary):
```
HTTP/1.1 200 OK
Date: Thu, 25 Sep 2025 23:06:15 GMT
Content-Type: text/html; charset=UTF-8
Content-Length: 342
Set-Cookie: coursename=CompNet; Path=/; HttpOnly; Max-Age=604800
Connection: close

<!DOCTYPE html>
<html lang="en"> ... (body truncated)
```

---

## Project Files Overview

- **`tcp_http_web_server.py`**  
  The main script that:
  1. Opens a TCP socket on `port = 12345`
  2. Accepts a connection and reads the HTTP request
  3. Builds a `200 OK` response with headers and a cookie
  4. Sends the contents of `html_files/index.html`
  5. On error, returns a minimal `404 Not Found` response

- **`html_files/index.html`**  
  A minimal example HTML page served by the server:
  ```html
  <!DOCTYPE html>
  <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>TCP Web Server Test</title>
    </head>
    <body>
      <b>TCP/HTTP Socket Web Server</b>
      <p>This is a simple static page served by a Python socket-based HTTP server.</p>
    </body>
  </html>
  ```

---

## How It Works (High Level)

1. **Socket Setup** — `socket(AF_INET, SOCK_STREAM)` creates a TCP socket bound to `0.0.0.0:12345`.
2. **Listen & Accept** — The server listens for one connection at a time and accepts a client.
3. **Request Parsing (Minimal)** — Reads request bytes and extracts the path token (e.g., `GET / HTTP/1.1`).
4. **Response Construction** — Builds standard headers, sets a cookie (`coursename=CompNet`) with `Max-Age=604800`, and declares `Content-Type` and `Content-Length`.
5. **Body Send** — Sends the HTML page from `./html_files/index.html`.
6. **Error Handling** — If the file is missing, returns a `404 Not Found` with a minimal HTML body.

---

## Customization

- **Port** — Change `port = 12345` at the top of `tcp_http_web_server.py`.
- **Default Page** — Replace `html_files/index.html` with your content.
- **Cookie** — Adjust the `Set-Cookie` header value. The included code uses:
  ```
  Set-Cookie: coursename=CompNet; Path=/; HttpOnly; Max-Age=604800
  ```
  - `HttpOnly` prevents JavaScript access to the cookie.
  - `Max-Age=604800` sets an expiry of 7 days.
  - Add `SameSite=Lax` or `SameSite=Strict` if you want to control cross-site sending behavior.

---

## Known Limitations (Intentional for Coursework)

- **Single-threaded:** Handles one connection at a time. No concurrency.
- **Minimal parsing:** Assumes well-formed `GET` requests and a present path token.
- **Fixed file:** The current example always serves `html_files/index.html` regardless of the path.
- **Path traversal hardening not implemented:** The code does not normalize/validate user-supplied paths.
- **UTF‑8 byte length vs. per-char send:** The script computes `Content-Length` from UTF‑8 bytes but then sends the body character-by-character (`.encode()` per character). For non‑ASCII pages, this may mismatch header/body byte counts. A safer pattern is to send the full `output_bytes` at once:

  ```python
  # After computing output_bytes = outputdata.encode('utf-8')
  connectionSocket.sendall(output_bytes)
  ```

These limitations are acceptable for demonstrating basic TCP/HTTP mechanics. For production use, prefer a real HTTP server or a framework (e.g., `http.server`, Flask, FastAPI, etc.).

---

## Troubleshooting

- **Port already in use:** Change `port = 12345` or stop the conflicting process.
- **Nothing loads in browser:** Confirm the server is running and you’re visiting `http://127.0.0.1:12345/` (not HTTPS).
- **Permission issues on Linux/macOS:** Try `python3 tcp_http_web_server.py` and ensure the file has read permissions.

---

## References

- Python `socket` library (stdlib)
- HTTP/1.1 message format (status line, headers, CRLF, body)
- Cookie attributes: `HttpOnly`, `Max-Age`, `Path`, and optional `SameSite`

---

## License

For coursework and educational use.
