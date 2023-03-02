from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import httpx
from httpx import AsyncClient
from fastapi import Request
from fastapi.responses import StreamingResponse
from starlette.background import BackgroundTask

from utils import HttpUrlRedirectMiddleware

origins = ["*"]

app = FastAPI()

app.add_middleware(HttpUrlRedirectMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

HTTP_SERVER = AsyncClient(base_url="http://116.86.210.54:5678/")
# HTTP_SERVER = AsyncClient(base_url="http://localhost:57800/")

async def _reverse_proxy(request: Request):
    url = httpx.URL(path=request.url.path, query=request.url.query.encode("utf-8"))
    rp_req = HTTP_SERVER.build_request(
        request.method, url, headers=request.headers.raw, content=await request.body(),timeout=120
    )
    rp_resp = await HTTP_SERVER.send(rp_req, stream=True)
    return StreamingResponse(
        rp_resp.aiter_raw(),
        status_code=rp_resp.status_code,
        headers=rp_resp.headers,
        background=BackgroundTask(rp_resp.aclose),
    )

app.add_route("/{path:path}", _reverse_proxy, ["GET", "POST"])