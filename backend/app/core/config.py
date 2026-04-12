import os
from dotenv import load_dotenv

# Carrega as variáveis do ficheiro .env
load_dotenv()

class Settings:
    PROJECT_NAME: str = "Pix Vending Machine"
    
    # Busca da variável de ambiente ou usa None como padrão
    MP_TOKEN_TESTE = os.getenv("MP_ACCESS_TOKEN_TESTE")
    MP_TOKEN_PRODUCAO = os.getenv("MP_ACCESS_TOKEN_PRODUCAO")
    
    # Escolha automática do token (mude para True quando quiser produção)
    USE_PROD = True 
    
    @property
    def mp_token(self):
        return self.MP_TOKEN_PRODUCAO if self.USE_PROD else self.MP_TOKEN_TESTE

settings = Settings()