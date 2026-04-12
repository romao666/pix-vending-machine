from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import mercadopago
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

# 1. Configuração de CORS (Essencial para o Frontend funcionar)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

sdk = mercadopago.SDK(settings.mp_token)

# Banco de dados temporário em memória
db_pagamentos = {}

@app.get("/")
def read_root():
    return {"status": "Vending Machine API Online"}

# 2. Rota que o Frontend vai chamar para gerar o QR Code
@app.post("/gerar-pagamento")
async def gerar_pagamento():
    payment_data = {
        "transaction_amount": 0.01, # Valor fixo para teste
        "description": "Vending Machine Item A1",
        "payment_method_id": "pix",
        "payer": {"email": "cliente@vending.com"}
    }
    
    result = sdk.payment().create(payment_data)
    payment = result["response"]
    
    if "id" in payment:
        p_id = str(payment["id"])
        db_pagamentos[p_id] = "pending" # Registra no nosso "banco"
        
        return {
            "id": p_id,
            "qr_code": payment["point_of_interaction"]["transaction_data"]["qr_code"],
            "qr_code_base64": payment["point_of_interaction"]["transaction_data"]["qr_code_base64"]
        }
    raise HTTPException(status_code=400, detail="Erro ao gerar pagamento")

# 3. Rota que o Frontend vai consultar (Polling) para saber se já foi pago
@app.get("/status/{payment_id}")
async def verificar_status(payment_id: str):
    return {"status": db_pagamentos.get(payment_id, "not_found")}

# 4. Webhook que recebe a confirmação do Mercado Pago
@app.post("/webhook")
async def webhook(request: Request):
    payload = await request.json()
    
    if payload.get("type") == "payment":
        p_id = str(payload["data"]["id"])
        
        # Validação de Segurança
        payment_info = sdk.payment().get(p_id)
        status = payment_info["response"].get("status")
        
        if status == "approved":
            print(f"✅ Pagamento {p_id} APROVADO!")
            db_pagamentos[p_id] = "approved"
            # TODO: Futuramente disparar MQTT aqui
            
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)