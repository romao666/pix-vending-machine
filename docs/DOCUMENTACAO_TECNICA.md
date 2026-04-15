# Documentação Técnica: Cherry Bomb Handmade 🍒

## 1. Visão Geral do Sistema
O **Cherry Bomb Handmade** é um sistema de automação para *vending machines* focado na venda de produtos artesanais. O projeto opera em um modelo "Mobile-First": o usuário interage via web app escaneando um QR Code colado na máquina e realiza o pagamento exclusivamente via Pix. Não há uso de dinheiro físico ou maquininhas de cartão.

## 2. Arquitetura de Software (Concluída/Em Produção)
O ecossistema é dividido em 3 camadas principais, totalmente funcionais:

### 2.1. Backend (FastAPI / Python)
Hospedado no **Railway**, atua como o cérebro das transações.
* **Framework:** FastAPI (Python 3.11).
* **Banco de Dados:** PostgreSQL (Tabelas: `produtos` e `pagamentos`).
* **Integrações:** Mercado Pago (Geração e Webhook Pix) e Cloudinary (Hospedagem de imagens).

### 2.2. Frontend Cliente (HTML/JS/Tailwind)
Hospedado no **GitHub Pages**, é a interface de compra.
* **Gestão de Estado:** Carrinho dinâmico mantido em memória no navegador.
* **Fluxo:** Exibe a grade de produtos via `GET /produtos`, permite a seleção de múltiplos itens, e gera um Pix consolidado via `POST /gerar-pagamento`.
* **Polling:** Checa automaticamente a confirmação do pagamento a cada 3 segundos.

### 2.3. Frontend Administrativo (Painel Admin)
* **Funcionalidades:** Edição de inventário (preço, nome, quantidade) e upload direto de fotos para o Cloudinary.
* **Segurança:** Protegido por senha global (`x-admin-password`).

## 3. Arquitetura de Hardware e Integração (Fase de Prototipagem)
O sistema foi desenhado para integrar a nuvem com o hardware físico através do protocolo **MQTT**.

* **Microcontrolador Base:** ESP32 WROOM-32 DevKit.
* **Motores e Drivers:** Motores DC TT (30-90 RPM) controlados por drivers TB6612FNG.
* **Protocolo:** Quando o webhook do Mercado Pago aprova o pagamento, o backend deve publicar uma matriz de liberação em um tópico MQTT (ex: `vending/dispense`). O ESP32 assina esse tópico e aciona os motores correspondentes.

---

## ⚠️ 4. Pontos de Atenção para a Engenharia de Hardware
*(Área destinada aos técnicos de eletrônica e engenheiros de hardware)*

O software já está pronto para emitir comandos de liberação, mas a construção física precisa resolver os seguintes desafios técnicos:

### A. Limitação de Pinos (GPIO) do ESP32
O projeto prevê até 20 motores na máquina final. Cada driver de motor TB6612FNG exige múltiplos pinos de controle (PWM, IN1, IN2). O ESP32 WROOM-32 **não possui portas lógicas suficientes** para controlar 20 motores diretamente.
* **Solução necessária:** O técnico deverá projetar uma placa/circuito utilizando **expansores de I/O** (como o chip MCP23017 ou 74HC595) ou **módulos controladores PWM** (como o PCA9685).

### B. Infraestrutura e Topologia do Broker MQTT
A comunicação entre o Backend no Railway e o ESP32 exige um "Broker MQTT" para rotear as mensagens.
* **Decisão necessária:** Definir se o broker será um serviço na nuvem (ex: HiveMQ, AWS IoT) ou um servidor local rodando na mesma rede Wi-Fi da máquina (ex: um Raspberry Pi com Mosquitto). A escolha afeta a latência e a dependência de internet da máquina.

### C. Tratamento de Falha Físicas (Sensor de Queda)
Atualmente, o estoque é descontado assim que o Pix é aprovado.
* **Definição de Fallback:** É necessário planejar um mecanismo de verificação física (como uma barreira infravermelha de sensor de queda). Se o ESP32 girar a mola e o produto agarrar/não cair, o hardware deve ter uma rotina para: 
  1) Tentar girar novamente.
  2) Em caso de falha definitiva, notificar o backend para alertar o admin ou processar um estorno automático do Pix.

---
*Documentação gerada para alinhamento entre equipes de Software e Hardware.*
