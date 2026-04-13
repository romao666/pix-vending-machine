# 🍒 Especificações de Identidade Visual e UI/UX (IV_DESIGN.md)

## 1. Visão Geral da Marca
* **Nome:** Cherry Bomb Handmade
* **Conceito:** Vending machine de artesanatos autênticos via QR Code e PIX.
* **Estética Core:** Y2K (anos 2000), Pop-Punk, Neobrutalismo focado em Polaroids.
* **Tom de Voz:** Direto, moderno e autêntico.
* **Abordagem UI:** Mobile-First absoluto (acesso exclusivo via QR code na máquina). Sem efeitos de "hover" ou "zoom", interface 100% estática e focada no toque (`:active` only).

---

## 2. Paleta de Cores (Bicolor Estrito)
A paleta é restrita a 4 cores. **Rosa é expressamente proibido.**

| Cor | Hex | Uso |
|-----|-----|-----|
| Vermelho Cereja Vibrante | `#C8102E` | Header, fundo de modais, botões ADD |
| Vermelho Escuro | `#8B0000` | Footer da sacola, botão lixeira/X, botão Sacola |
| Branco Puro | `#FFFFFF` | Cards, fundos, textos sobre vermelho |
| Preto Sólido | `#1A1A1A` | Bordas, textos, badges de localização |

---

## 3. Tipografia
* **Display (Títulos e Marcas):** `Shrikhand` — Header, telas de impacto (Quase lá!, Pagamento Aprovado!)
* **Interface (Corpo e Botões):** `Poppins` — Nomes de produtos, preços, botões, controles

---

## 4. Assets
* **logo.svg** — Logo principal com traços brancos (uso sobre fundo vermelho)
* **logo-red.svg** — Logo com traços vermelhos (uso sobre fundo branco, ex: tela de login do admin)

---

## 5. Componentes de Interface (Polaroid Neobrutalista)

### Regras Globais
- Bordas sólidas pretas `2px solid #1A1A1A` em todos os elementos
- Sombras sólidas sem desfoque: `4px 4px 0px #1A1A1A` (brutal) e `2px 2px 0px #1A1A1A` (brutal-sm)
- **Sem bordas arredondadas**
- **Sem hover** — apenas `:active` com `transform: scale(0.95)`

### Cards de Produto (Polaroid)
- Fundo branco, formato vertical
- Foto real do produto (Cloudinary) ou emoji 📦 como fallback
- Badge de localização sobreposto no canto superior esquerdo da foto
- Badge: fundo `#1A1A1A`, texto branco, fonte Poppins bold
- Nome em Shrikhand abaixo da foto
- Preço em `#C8102E` abaixo do nome
- Botão ADD vermelho cereja largura total

### Controles Dinâmicos
- **Estado 1 (vazio):** Botão `ADD` vermelho cereja (`#C8102E`)
- **Estado 2 (selecionado):** Seletor `[ ✕ ] [ − ] [ Qtd ] [ + ]`
- Botão `✕` usa vermelho escuro (`#8B0000`) — ação destrutiva
- Botão `+` trava visualmente (opacity 0.3) ao atingir limite de estoque

### Header (Frontend)
- Fundo `#C8102E`, borda inferior `4px solid #1A1A1A`
- Logo SVG (branca) + texto "Cherry Bomb" + "— HANDMADE —" em linha horizontal

### Footer (Sacola Fixa)
- Fundo branco, borda superior `4px solid #1A1A1A`
- Subtotal em vermelho cereja à esquerda
- Botão Sacola com fundo `#8B0000` e ícone SVG à direita

### Bottom Sheet (Sacola)
- Sem bordas arredondadas
- Borda superior `4px solid #1A1A1A`
- Botão "Limpar" vermelho escuro + botão "✕" branco no header
- Itens listados com nome, localização, quantidade e valor

### Tela de Pagamento
- Fundo `#C8102E` fullscreen
- Título "Quase lá!" em Shrikhand branco
- Card branco central com QR Code real, valor, código Pix e botão copiar preto
- Status "⏳ Aguardando confirmação..." em fundo amarelo claro

### Tela de Sucesso
- Fundo `#C8102E` fullscreen
- Partículas de cerejas e estrelas caindo (animação CSS)
- Título "Pagamento Aprovado!" em Shrikhand branco
- Card branco com instrução de retirada
- Logo SVG no rodapé
- Botão "Fazer novo pedido" vermelho escuro

### Painel Admin
- Tela de login: fundo vermelho cereja, card branco central, logo-red.svg
- Header: fundo vermelho cereja, logo + "Admin" + botão "Sair" vermelho escuro
- Lista de produtos: cards com foto, badge de posição, nome, preço, estoque e botão "Editar"
- Modal de edição: preview de foto, campos de nome/preço/estoque, input file customizado
- Botão atualizar: ícone SVG de refresh sem emoji

---

## 6. Fluxo de Telas (Mobile — Frontend Cliente)

### Tela 1: Vitrine (Home)
- Header com logo + "Cherry Bomb" + "— HANDMADE —"
- Grid de **4 colunas × 5 linhas (A1→E4)** renderizado dinamicamente via API
- Fotos reais dos produtos via Cloudinary, fallback 📦
- Items esgotados: opacity 0.45, grayscale 60%, pointer-events none
- Footer fixo com subtotal dinâmico e botão Sacola

### Tela 2: Bottom Sheet — Sacola
- Desliza de baixo para cima sobre a vitrine
- Lista dinâmica dos itens do carrinho
- Total calculado em tempo real
- Botões: "Ir para Pagamento" e "Continuar Comprando"

### Tela 3: Pagamento (Checkout PIX)
- Gerado via `POST /gerar-pagamento` com itens reais
- QR Code renderizado via base64
- Polling a cada 3s em `GET /status/{id}`

### Tela 4: Confirmação (Sucesso)
- Disparada automaticamente pelo polling ao detectar `approved`
- Animação de cerejas e estrelas caindo
- Botão "Fazer novo pedido" reseta o app

---

## 7. Lógica de Negócio (Frontend)
- Cards renderizados dinamicamente via `GET /produtos`
- Carrinho gerenciado em memória com `data-id` por card
- Subtotal atualizado em tempo real a cada interação
- Botão `+` bloqueado ao atingir limite de estoque
- Polling de 3s detecta aprovação sem refresh manual
- Reset completo do app após novo pedido