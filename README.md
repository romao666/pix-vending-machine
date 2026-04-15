# 🍒 Cherry Bomb Handmade - Vending Machine

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-lightgrey.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Sistema de automação inteligente para vending machines de produtos artesanais, integrando pagamentos instantâneos via Pix e controle de hardware via ESP32.

## 📌 Sobre o Projeto
O **Cherry Bomb Handmade** é uma solução completa de hardware e software para democratizar a venda de artesanatos. Através de uma interface web intuitiva, o cliente realiza a compra via Pix e a máquina libera o produto automaticamente.

## 🛠️ Tecnologias Utilizadas
- **Backend:** Python & Flask
- **Pagamentos:** API Mercado Pago (Pix)
- **Hardware:** ESP32 & Motores de Passo
- **Interface:** HTML5/CSS3 com estética Neobrutalista

## 🚀 Funcionalidades
- [x] Geração de QR Code Pix dinâmico.
- [x] Verificação de pagamento em tempo real.
- [x] Interface mobile-first para seleção de produtos.
- [ ] Integração total com firmware ESP32 (Em desenvolvimento).
- [ ] Sensores de queda de produto (Roadmap).

## 🔧 Configuração e Instalação
1. Clone o repositório:
   ```bash
   git clone [https://github.com/joaoromaodev/pix-vending-machine.git](https://github.com/joaoromaodev/pix-vending-machine.git)
   
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   
3. Configure suas credenciais do Mercado Pago no arquivo **.env**

4. Execute o servidor:
   ```bash
   python app.py 

## 🏗️ Hardware
O projeto utiliza um ESP32 para controlar a parte mecânica. Os detalhes da carcaça e especificações de motores estão atualmente na fase de prototipagem (À definir).

## Desenvolvido por João Romão
