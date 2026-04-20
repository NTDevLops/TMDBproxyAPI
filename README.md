-----

# 🎬 TMDB Proxy API

A lightweight, high-performance proxy server designed to bridge requests to **The Movie Database (TMDB)**. This tool allows you to mask TMDB endpoints and serve images through your own domain, bypassing potential CORS issues or domain restrictions.

-----

## ✨ Key Features

  * **🖼️ Image CDN Proxy:** Seamlessly mirrors the TMDB Image CDN.
  * **🎬 API Gateway:** Forwards requests to the official TMDB API v3/v4.
  * **⚡ High Performance:** Built on **FastAPI** and **HTTPX** for asynchronous, non-blocking I/O.
  * **🐳 Containerized:** Ready for instant deployment via Docker.
  * **🔒 Stateless:** Does not store keys or logs, ensuring privacy.

-----

## 🛠️ How It Works

### 1\. Image Proxying

The proxy intercepts image requests and fetches them directly from `image.tmdb.org`.

| Request Path | Becomes (Upstream) |
| :--- | :--- |
| `/image/t/p/w500/abc.jpg` | `https://image.tmdb.org/t/p/w500/abc.jpg` |

### 2\. Data API Proxying

The proxy forwards metadata requests to `api.themoviedb.org`.

| Request Path | Becomes (Upstream) |
| :--- | :--- |
| `/info-api/3/movie/popular` | `https://api.themoviedb.org/3/movie/popular` |

-----

## 🚀 Quick Start

### Local Setup

1.  **Clone the repo**

    ```bash
    git clone https://github.com/your-username/tmdb-proxy.git
    cd tmdb-proxy
    ```

2.  **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Launch Server**

    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ```

### Docker Setup

```bash
docker build -t tmdb-proxy .
docker run -d -p 8000:8000 tmdb-proxy
```

-----

## 📡 API Reference

### Get Movie/TV Info

`GET /info-api/{version}/{endpoint}`

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `version` | `int` | TMDB API version (e.g., `3`) |
| `endpoint` | `string` | The API path (e.g., `movie/popular`) |
| `api_key` | `query` | **Required.** Your TMDB API Key |

**Example:**
`http://localhost:8000/info-api/3/movie/550?api_key=YOUR_KEY`

### Get Images

`GET /image/t/p/{size}/{file_path}`

**Example:**
`http://localhost:8000/image/t/p/original/h8m0uS9zZ9vXp3ZqE6ZfXv1p.jpg`

-----

## 🏗️ Project Structure

```text
.
├── main.py            # Main FastAPI application logic
├── requirements.txt   # Python package dependencies
├── Dockerfile         # Container orchestration
└── README.md          # Documentation
```

-----

## 🔐 Security & Optimization

> [\!IMPORTANT]
> **API Keys:** This proxy requires the `api_key` to be passed in the query string from the client. For production, consider modifying the code to inject the API key as an Environment Variable to keep it hidden from the frontend.

  * **Caching:** It is highly recommended to put **Nginx** or **Cloudflare** in front of this service to cache image blobs and reduce upstream hits.
  * **Rate Limiting:** If deploying publicly, implement `slowapi` or Nginx `limit_req` to prevent abuse.

-----

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

-----

**Disclaimer:** *This project is not affiliated with, maintained by, or endorsed by The Movie Database (TMDB). It is a utility tool intended for developer use.*