from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import mercadopago
from app.core.config import settings
from app.routers import produtos, pagamento

app = FastAPI(title="Cherry Bomb Handmade — API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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
            # TODO: remover em produção
            print(f"🧪 Forçando aprovação para teste: {p_id}")
            db_pagamentos[p_id] = "approved"

    return {"status": "ok"}