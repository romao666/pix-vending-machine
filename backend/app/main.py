from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import mercadopago
import os
from app.core.config import settings
from app.core.database import init_db
from app.routers import produtos, pagamento, admin

app = FastAPI(title="Cherry Bomb Handmade — API")

# Origens da vitrine, separadas por virgula em ALLOWED_ORIGINS.
# Sem a variavel o comportamento antigo continua (qualquer origem), para nao
# derrubar a loja — mas nesse caso o header do painel admin nao entra na lista
# permitida, entao nenhum site aleatorio consegue dirigir o /admin pelo
# navegador de quem estiver logado. Definir ALLOWED_ORIGINS libera o painel de
# novo, so que restrito as origens declaradas.
#
# CORS nao e autenticacao: cliente que nao seja navegador ignora tudo isto. A
# protecao real do /admin continua sendo a senha em ADMIN_PASSWORD.
ALLOWED_ORIGINS = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "").split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS or ["*"],
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=(
        ["Content-Type", "x-admin-password"]
        if ALLOWED_ORIGINS
        else ["Content-Type"]
    ),
)

sdk = mercadopago.SDK(settings.mp_token)

app.include_router(produtos.router)
app.include_router(pagamento.router)
app.include_router(admin.router)


@app.on_event("startup")
def startup():
    init_db()
    print("🍒 Cherry Bomb API iniciada — banco SQLite pronto")


@app.get("/")
def read_root():
    return {"status": "Cherry Bomb API Online 🍒"}


@app.post("/webhook")
async def webhook(request: Request):
    payload = await request.json()

    if payload.get("type") == "payment":
        p_id = str(payload["data"]["id"])

        payment_info = sdk.payment().get(p_id)
        status = payment_info["response"].get("status")

        print(f"📦 Pagamento {p_id} — status: {status}")

        if status == "approved":
            print(f"✅ Pagamento {p_id} APROVADO!")
            from app.routers.pagamento import aprovar_pagamento
            aprovar_pagamento(p_id)
        else:
            print(f"⏳ Pagamento {p_id} ainda não aprovado — status: {status}")

    return {"status": "ok"}