from fastapi import FastAPI, Request, Response
from fastapi.responses import StreamingResponse
import httpx

app = FastAPI()

TMDB_IMAGE_BASE = "https://image.tmdb.org"
TMDB_API_BASE = "https://api.themoviedb.org"

client = httpx.AsyncClient(
    http2=True,
    timeout=10,
    limits=httpx.Limits(
        max_connections=100,
        max_keepalive_connections=20
    )
)


@app.get("/")
async def root():
    return {
        "name": "TMDB Proxy API",
        "status": "running",
    }


@app.get("/image/{full_path:path}")
async def image_proxy(full_path: str):
    url = f"{TMDB_IMAGE_BASE}/t/p/{full_path}"

    r = await client.get(url)

    if r.status_code != 200:
        return Response("Image fetch failed", status_code=502)

    return StreamingResponse(
        r.aiter_bytes(),
        media_type=r.headers.get("content-type", "image/jpeg"),
        headers={
            "Cache-Control": "public, max-age=86400, stale-while-revalidate=604800",
            "Access-Control-Allow-Origin": "*"
        }
    )


@app.get("/info-api/{full_path:path}")
async def tmdb_api_proxy(request: Request, full_path: str):
    r = await client.get(
        f"{TMDB_API_BASE}/{full_path}",
        params=request.query_params,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    return Response(
        content=r.content,
        media_type="application/json",
        headers={
            "Access-Control-Allow-Origin": "*",
            "Cache-Control": "public, max-age=60, stale-while-revalidate=300"
        }
    )
