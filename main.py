from fastapi import FastAPI, Request, Response
import httpx
from contextlib import asynccontextmanager

TMDB_IMAGE_BASE = "https://image.tmdb.org"
TMDB_API_BASE = "https://api.themoviedb.org"


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with httpx.AsyncClient(
        http2=True,
        timeout=httpx.Timeout(5.0, connect=2.0),
        limits=httpx.Limits(
            max_connections=1000,
            max_keepalive_connections=300
        ),
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept-Encoding": "gzip, br"
        }
    ) as client:
        app.state.client = client
        yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"name": "TMDB Proxy API", "status": "running"}


@app.get("/image/{full_path:path}")
async def image_proxy(request: Request, full_path: str):
    client: httpx.AsyncClient = request.app.state.client
    url = f"{TMDB_IMAGE_BASE}/t/p/{full_path}"

    try:
        r = await client.get(url)
    except httpx.RequestError:
        return Response("Upstream error", status_code=502)

    if r.status_code != 200:
        return Response("Image fetch failed", status_code=502)

    return Response(
        content=r.content,
        media_type=r.headers.get("content-type", "image/jpeg"),
        headers={
            "Cache-Control": "public, max-age=86400, stale-while-revalidate=604800",
            "Access-Control-Allow-Origin": "*"
        }
    )


@app.get("/info-api/{full_path:path}")
async def tmdb_api_proxy(request: Request, full_path: str):
    client: httpx.AsyncClient = request.app.state.client
    url = f"{TMDB_API_BASE}/{full_path}"

    try:
        r = await client.request(
            method="GET",
            url=url,
            params=request.query_params,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )
    except httpx.RequestError:
        return Response("Upstream error", status_code=502)

    if r.status_code != 200:
        return Response("API fetch failed", status_code=502)

    return Response(
        content=r.content,
        media_type="application/json",
        headers={
            "Access-Control-Allow-Origin": "*",
            "Cache-Control": "public, max-age=60, stale-while-revalidate=300"
        }
    )
