import sys
import os

# Adiciona a pasta backend ao path para conseguirmos importar o config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import mercadopago
from app.core.config import settings

def gerar_cobranca():
    # Agora usamos o token que vem do .env de forma segura
    sdk = mercadopago.SDK(settings.mp_token)

    payment_data = {
        "transaction_amount": 0.01,
        "description": "Vending Machine - Teste Seguro",
        "payment_method_id": "pix",
        "payer": {"email": "seu-email@exemplo.com"}
    }

    print(f"Gerando Pix usando ambiente de {'PRODUÇÃO' if settings.USE_PROD else 'TESTE'}...")
    
    result = sdk.payment().create(payment_data)
    payment = result["response"]

    if "id" in payment:
        print(f"✅ Sucesso! ID: {payment.get('id')}")
        print(f"Pix Copia e Cola: {payment['point_of_interaction']['transaction_data']['qr_code']}")
    else:
        print("❌ Erro na geração.")

if __name__ == "__main__":
    gerar_cobranca()