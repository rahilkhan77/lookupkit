from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import assert_stripe_safe, settings
from app.db import init_db
from app.routers import account, auth, billing, v1


@asynccontextmanager
async def lifespan(_: FastAPI):
    assert_stripe_safe()
    init_db()
    yield


app = FastAPI(
    title="Lookupkit API",
    version="0.1.0",
    description="Phone, email, and IP verification. A Keystone product by Excentia.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.web_origin, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(account.router)
app.include_router(billing.router)
app.include_router(v1.router)


@app.get("/healthz")
def healthz():
    return {"ok": True}
