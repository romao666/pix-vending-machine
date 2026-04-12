# 🍒 Especificações de Identidade Visual e UI/UX (IV_DESIGN.md)

## 1. Visão Geral da Marca
* **Nome:** Cherry Bomb Handmade
* **Conceito:** Vending machine de artesanatos autênticos via QR Code e PIX.
* **Estética Core:** Y2K (anos 2000), Pop-Punk, Contraste Marcante.
* **Tom de Voz:** Direto, moderno e autêntico.
* **Abordagem UI:** Mobile-First absoluto (acesso exclusivo via QR code na máquina).

---

## 2. Paleta de Cores (Contraste Máximo)
* **Cor Primária:** `#C8102E` (Vermelho Cereja Vibrante) - Uso em fundos de tela e headers.
* **Cor Secundária:** `#FFFFFF` (Branco Puro) - Uso em cards, modais e fundos de texto.
* **Cor de Destaque:** `#FF1493` (Deep Pink) - Uso em botões e ícones de ação.
* **Contraste/Bordas:** `#1A1A1A` (Preto Sólido) - Uso em textos e contornos neobrutalistas.

---

## 3. Tipografia (Google Fonts)
* **Display (Títulos e Marcas):** `Shrikhand` ou `Bangers`.
  * *Uso:* Nome da marca e títulos de impacto (Ex: "Quase lá! 🍒").
* **Interface (Corpo e Botões):** `Poppins` ou `Outfit`.
  * *Uso:* Nomes de produtos, preços, botões e informações de estoque.

---

## 4. Componentes de Interface (Estilo Neobrutalista)
* **Estilo Geral:** Bordas sólidas pretas de `2px` em todos os elementos. Sombras projetadas (`box-shadow`) pretas e sólidas (sem desfoque).
* **Cards de Produto:** * Badge de localização (ex: A1, B4) em destaque preto com texto branco.
  * Botões de controle de quantidade (+ / -) integrados ao card.
* **Botões:** Formato pílula ou bordas arredondadas (12px). Feedback tátil via CSS `transform: scale(0.95)` ao clicar.

---

## 5. Fluxo de Telas (Mobile)

### Tela 1: Vitrine (Home)
* **Header:** Logo centralizada sobre fundo Vermelho.
* **Body:** Grid de 2 colunas com produtos. Itens sem estoque devem aparecer translúcidos com aviso "Esgotado".
* **Sacola:** Barra fixa inferior mostrando o valor total e o botão "Checkout".

### Tela 2: Sacola (Revisão)
* **Apresentação:** Bottom Sheet (desliza de baixo para cima) sobrepondo a vitrine.
* **Lista:** Resumo dos itens com opção de alteração final.
* **Ação:** Botão "Ir para Pagamento".

### Tela 3: Pagamento (Checkout PIX)
* **Visual:** Fundo vermelho.
* **Título:** "Quase lá! 🍒" (Fonte de Display).
* **Subtítulo:** "Finalize o pagamento via Pix para liberar seu pedido."
* **Elementos:** Card branco central com QR Code, botão "Copiar Código Pix" e indicador de "Aguardando confirmação...".

### Tela 4: Confirmação (Sucesso)
* **Gatilho:** Ativada automaticamente via polling de status (`approved`).
* **Visual:** Animação de sucesso (brilhos/cerejas).
* **Copywriting:** "Pagamento Aprovado! 🍒"
* **Instrução:** "Aguarde o giro das molas e retire seus mimos abaixo."

---

## 6. Lógica de Negócio (Frontend)
* Bloqueio automático de adição de itens caso exceda o estoque disponível em tempo real.
* Polling (consulta recorrente) ao backend a cada 3 segundos para detectar a aprovação do pagamento sem necessidade de atualização manual da página.