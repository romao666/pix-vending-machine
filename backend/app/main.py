from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import mercadopago
from app.core.config import settings
from app.routers import produtos, pagamento

app = FastAPI(title="Cherry Bomb Handmade — API")

from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request as StarletteRequest

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class NgrokMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: StarletteRequest, call_next):
        response = await call_next(request)
        return response

app.add_middleware(NgrokMiddleware)

sdk = mercadopago.SDK(settings.mp_token)

app.include_router(produtos.router)
app.include_router(pagamento.router)


@app.get("/")
def read_root():
    return {"status": "Cherry Bomb API Online 🍒"}


@app.post("/webhook")
async def webhook(request: Request):
    payload = await request.json()

    if payload.get("type") == "payment":
        p_id = str(payload["data"]["id"])

        from app.routers.pagamento import db_pagamentos

        # Valida com Mercado Pago
        payment_info = sdk.payment().get(p_id)
        status = payment_info["response"].get("status")

        print(f"📦 Pagamento {p_id} — status: {status}")

        if status == "approved":
            print(f"✅ Pagamento {p_id} APROVADO!")
            db_pagamentos[p_id] = "approved"
        else:
            print(f"⏳ Pagamento {p_id} ainda não aprovado — status: {status}")

    return {"status": "ok"}