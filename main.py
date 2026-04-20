from fastapi import FastAPI, Request, Response
import httpx

app = FastAPI()

TMDB_IMAGE_BASE = "https://image.tmdb.org"
TMDB_API_BASE = "https://api.themoviedb.org"

@app.get("/image/{full_path:path}")
async def image_proxy(full_path: str):
    target_url = f"{TMDB_IMAGE_BASE}/t/p/{full_path}"

    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(target_url)

    if r.status_code != 200:
        return Response("Image fetch failed", status_code=502)

    return Response(
        content=r.content,
        media_type=r.headers.get("content-type", "image/jpeg"),
        headers={
            "Cache-Control": "public, max-age=86400",
            "Access-Control-Allow-Origin": "*"
        }
    )

@app.api_route("/info-api/{full_path:path}", methods=["GET"])
async def tmdb_api_proxy(request: Request, full_path: str):
    query = request.url.query

    target_url = f"{TMDB_API_BASE}/{full_path}"
    if query:
        target_url += f"?{query}"

    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(
            target_url,
            headers={"User-Agent": "Mozilla/5.0"}
        )

    return Response(
        content=r.content,
        media_type="application/json",
        headers={
            "Access-Control-Allow-Origin": "*",
            "Cache-Control": "no-store"
        }
    )