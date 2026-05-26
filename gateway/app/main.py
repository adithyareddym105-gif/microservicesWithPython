from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
import httpx

app = FastAPI()

# Route table — add new services here
ROUTES = {
    "users": "http://localhost:8001",
    "games": "http://localhost:8002",
    "activities": "http://localhost:8003",
}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.api_route("/v1/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(path: str, request: Request):

    # Step 1 — extract the resource name
    resource = path.split("/")[0]

    # Step 2 — look up route
    base_url = ROUTES.get(resource)

    if not base_url:
        return JSONResponse(
            status_code=404, content={"detail": f"Unknown resource: {resource}"}
        )

    # Step 3 — build target URL
    target_url = f"{base_url}/v1/{path}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=request.method,
                url=target_url,
                headers={
                    k: v for k, v in request.headers.items() if k.lower() != "host"
                },
                content=await request.body(),
                params=request.query_params,
                follow_redirects=True,
            )

        return Response(
            content=response.content,
            status_code=response.status_code,
            media_type=response.headers.get("content-type"),
        )

    except httpx.RequestError as e:
        return JSONResponse(
            status_code=503, content={"detail": f"Service unavailable: {str(e)}"}
        )
