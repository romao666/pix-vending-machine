# Documentação Técnica: Cherry Bomb Handmade 🍒

> Última atualização: Abril 2026
> Autor: João Romão — romaocr33@gmail.com

---

## 1. Visão Geral do Sistema

O **Cherry Bomb Handmade** é um sistema de automação para vending machines focado na venda de produtos artesanais. O projeto opera em um modelo "Mobile-First": o usuário interage via web app escaneando um QR Code colado na máquina e realiza o pagamento exclusivamente via Pix. Não há uso de dinheiro físico ou maquininhas de cartão.

### Fluxo Principal (Happy Path)

```
1. Cliente escaneia o QR Code físico colado no vidro da máquina
2. Acessa a vitrine mobile e seleciona produtos (grid 4×5, slots A1→E4)
3. Monta a sacola com múltiplos itens e quantidades
4. Sistema gera um único Pix Copia e Cola via Mercado Pago
5. Cliente realiza o pagamento no app do banco
6. Webhook do Mercado Pago confirma o pagamento ao backend
7. Backend subtrai o estoque e publica mensagem MQTT
8. ESP32 recebe o sinal e gira as molas físicas correspondentes
9. Cliente retira os produtos liberados pela máquina
```

---

## 2. Links de Produção

| Ambiente | URL |
|----------|-----|
| 🛍️ Vitrine (Cliente) | https://joaoromaodev.github.io/pix-vending-machine/ |
| 🔧 Painel Admin | https://joaoromaodev.github.io/pix-vending-machine/admin.html |
| ⚙️ API Backend | https://hearty-tranquility-production.up.railway.app |
| 📖 Docs da API (Swagger) | https://hearty-tranquility-production.up.railway.app/docs |
| 🐙 Repositório | https://github.com/joaoromaodev/pix-vending-machine |

---

## 3. Arquitetura de Software

O ecossistema é dividido em 3 camadas principais, todas em produção:

```
┌─────────────────────────────────────────────────────────┐
│                    CLIENTE (Mobile)                      │
│         GitHub Pages — index.html                        │
│    Grade 4×5 · Carrinho · Checkout Pix · Polling        │
└─────────────────────┬───────────────────────────────────┘
                      │ HTTP / REST
┌─────────────────────▼───────────────────────────────────┐
│                  BACKEND (Railway)                       │
│              FastAPI — Python 3.11                       │
│    /produtos · /gerar-pagamento · /status · /webhook    │
│              PostgreSQL · Cloudinary                     │
└──────────┬──────────────────────────┬───────────────────┘
           │ Webhook (HTTPS)          │ MQTT (em impl.)
┌──────────▼──────────┐   ┌──────────▼───────────────────┐
│   MERCADO PAGO      │   │      ESP32 (Hardware)         │
│   API Pix           │   │   Motores TT + TB6612FNG      │
└─────────────────────┘   └──────────────────────────────┘
```

### 3.1. Backend (FastAPI / Python)

Hospedado no **Railway**, atua como o cérebro das transações.

**Stack:**
- Framework: FastAPI (Python 3.11)
- Banco de Dados: PostgreSQL (Railway — persistência permanente)
- ORM: psycopg2 com RealDictCursor
- Hospedagem de imagens: Cloudinary

**Estrutura de routers:**

| Router | Arquivo | Responsabilidade |
|--------|---------|-----------------|
| Produtos | `routers/produtos.py` | `GET /produtos` e `GET /produtos/{id}` |
| Pagamento | `routers/pagamento.py` | `POST /gerar-pagamento` e `GET /status/{id}` |
| Admin | `routers/admin.py` | CRUD de produtos + upload de imagens |
| Webhook | `main.py` | `POST /webhook` — confirmação Mercado Pago |

**Tabelas do banco de dados:**

```sql
-- Produtos (20 slots A1→E4)
CREATE TABLE produtos (
    id TEXT PRIMARY KEY,        -- ex: "A1", "B3"
    name TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER DEFAULT 0,
    image_url TEXT DEFAULT NULL -- URL Cloudinary
);

-- Pagamentos
CREATE TABLE pagamentos (
    id TEXT PRIMARY KEY,        -- ID Mercado Pago
    status TEXT DEFAULT 'pending',
    itens TEXT NOT NULL,        -- JSON com itens do carrinho
    total REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Variáveis de ambiente (Railway):**

| Variável | Descrição |
|----------|-----------|
| `MP_ACCESS_TOKEN_PRODUCAO` | Token de produção Mercado Pago |
| `MP_ACCESS_TOKEN_TESTE` | Token de teste Mercado Pago |
| `ADMIN_PASSWORD` | Senha do painel administrativo |
| `CLOUDINARY_CLOUD_NAME` | Cloud name do Cloudinary |
| `CLOUDINARY_API_KEY` | API Key do Cloudinary |
| `CLOUDINARY_API_SECRET` | API Secret do Cloudinary |
| `DATABASE_URL` | URL de conexão PostgreSQL (referência automática Railway) |

### 3.2. Frontend Cliente

Hospedado no **GitHub Pages** (`/docs` branch `gh-pages`).

**Tecnologias:** HTML5 puro + Tailwind CSS via CDN + Vanilla JavaScript

**Funcionalidades implementadas:**
- Renderização dinâmica do grid 4×5 via `GET /produtos`
- Carrinho gerenciado em memória (sem localStorage)
- Seletor de quantidade com limite de estoque em tempo real
- Botão `+` bloqueado visualmente ao atingir o estoque máximo
- Checkout via `POST /gerar-pagamento` com valor real calculado
- QR Code renderizado via base64 retornado pelo backend
- Polling a cada 3 segundos em `GET /status/{id}`
- Tela de sucesso com animação de partículas ao confirmar pagamento
- Reset completo do app após novo pedido

**Identidade Visual — Y2K / Pop-Punk Neobrutalista:**

| Token | Valor | Uso |
|-------|-------|-----|
| `cereja` | `#C8102E` | Header, botões ADD, telas de pagamento |
| `escuro` | `#8B0000` | Footer, sacola, ações destrutivas |
| `brutalista` | `#1A1A1A` | Bordas, textos, badges |
| Branco | `#FFFFFF` | Cards, fundos |
| Shrikhand | Display | Títulos e telas de impacto |
| Poppins | Interface | Botões, preços, controles |

### 3.3. Painel Administrativo

Acessível em `/admin.html` — protegido por senha via header `x-admin-password`.

**Funcionalidades:**
- Login por senha com feedback de erro
- Listagem de todos os 20 produtos com foto, preço e estoque
- Modal de edição: nome, preço, estoque e upload de foto
- Preview da imagem antes de salvar
- Upload direto para Cloudinary com crop automático 400×400
- Toast de confirmação após salvar
- Botão de atualização da listagem

---

## 4. Arquitetura de Hardware

### 4.1. Componentes

| Componente | Modelo | Quantidade | Função |
|-----------|--------|-----------|--------|
| Microcontrolador | ESP32 WROOM-32 DevKit (38 pinos) | 1 | Cérebro do hardware — WiFi + controle dos motores |
| Motor | Motor TT DC 3-6V, 90RPM@3V, 1:48 | 20 (4 no protótipo) | Girar as molas físicas |
| Driver de motor | TB6612FNG Duplo Ponte H | 10 (2 no protótipo) | Controlar direção e velocidade dos motores |
| Protoboard | 830 pontos | 1 | Prototipagem sem solda |
| Fonte de alimentação | 5V 2A (protótipo) / 5V 10A (produção) | 1 | Alimentar ESP32 e motores |

### 4.2. Protocolo de Comunicação (MQTT)

Quando o pagamento é aprovado, o backend publica no tópico `vending/dispense`:

```json
{
  "transaction_id": "153718375671",
  "actions": [
    {"motor": "A1", "quantity": 2, "time_ms": 2500},
    {"motor": "E3", "quantity": 1, "time_ms": 2500}
  ]
}
```

O ESP32 assina o tópico, interpreta o JSON e aciona os drivers TB6612FNG correspondentes para girar cada motor pelo tempo especificado.

### 4.3. Mapeamento de Pinos (ESP32 → TB6612FNG)

> ⚠️ A ser definido durante a prototipagem. Com 20 motores serão necessários expansores de I/O (MCP23017 ou similar) pois o ESP32 não possui GPIOs suficientes para controlar todos diretamente.

---

## 5. Status do Desenvolvimento

### ✅ Concluído e em Produção

| Fase | Descrição |
|------|-----------|
| Fase 1 | Frontend base — paleta, grid 4×5, carrinho, telas de pagamento e sucesso |
| Fase 2 | Backend — endpoints de produtos e pagamento com valor real |
| Fase 3 | Integração frontend↔backend — QR Code real, polling de status |
| Fase 4 | Deploy Railway + webhook Mercado Pago em produção |
| Fase 5 | Admin + Cloudinary — upload de fotos, persistência com PostgreSQL |
| Fase 6 | Estoque real — subtração automática após pagamento aprovado |
| Fase 8 | Hospedagem frontend — GitHub Pages com favicon |

### ⏸️ Pausado — Aguardando Hardware

| Fase | Descrição | Bloqueio |
|------|-----------|---------|
| Fase 7 | MQTT — disparo para ESP32 após pagamento | Aguardando chegada dos componentes |

### 📋 Backlog

- Sensor de queda de produto (barreira infravermelha)
- Estorno automático via Mercado Pago em caso de falha mecânica
- Domínio personalizado
- Proteção da rota `/admin` por URL secreta
- Notificação ao admin quando estoque estiver baixo

---

## 6. Pontos de Atenção para Colaboradores de Hardware

### A. Limitação de Pinos GPIO do ESP32

O ESP32 WROOM-32 não possui GPIOs suficientes para controlar 20 motores diretamente. Cada driver TB6612FNG exige pinos de controle PWM, IN1 e IN2.

**Solução necessária:** Utilizar expansores de I/O como o **MCP23017** (via I2C) ou controladores PWM como o **PCA9685** para multiplexar os sinais de controle.

### B. Broker MQTT

A comunicação entre o Backend (Railway) e o ESP32 exige um broker MQTT intermediário.

**Opções:**
- **Nuvem:** HiveMQ (gratuito), AWS IoT, EMQX Cloud
- **Local:** Raspberry Pi com Mosquitto na mesma rede WiFi da máquina

A escolha afeta latência e dependência de internet. Se a internet cair, broker local mantém a máquina funcionando.

### C. Sensor de Queda (Fallback Físico)

Atualmente o estoque é descontado no momento da aprovação do Pix. Se o motor girar mas o produto travar/não cair, o cliente paga sem receber.

**Solução planejada:**
1. Sensor infravermelha na saída da mola detecta se o produto caiu
2. Se não detectar queda, o motor tenta novamente (até 3 tentativas)
3. Em caso de falha definitiva, backend é notificado para alertar o admin ou processar estorno automático

---

## 7. Como Contribuir

Se você tem experiência com ESP32, MQTT, firmware ou mecânica, sua contribuição é bem-vinda!

1. Leia o `README.md` para entender o projeto
2. Consulte o `docs/HARDWARE_INTERFACE.md` para o protocolo MQTT
3. Abra uma Issue descrevendo sua contribuição
4. Faça um Fork, implemente e abra um Pull Request

**Contato:** romaocr33@gmail.com | [LinkedIn](https://www.linkedin.com/in/joaoromao-data/)

---

*Documentação mantida por João Romão — Belém, PA, Brasil*
