# Especificação do Produto: Pix Vending Machine

## Visão Geral
Uma máquina de vendas automática para artesanatos, operada via Pix, instalada em ambientes condominiais. O sistema elimina a necessidade de dinheiro físico ou maquininhas de cartão, utilizando apenas QR Codes e uma interface web mobile.

## Fluxo Principal (Happy Path)
1. **Acesso:** Cliente escaneia o QR Code físico na máquina (URL única).
2. **Seleção:** Cliente navega por uma lista de produtos categorizados por localização física (ex: A1, B4).
3. **Carrinho:** Cliente adiciona múltiplos itens e quantidades à sacola.
4. **Checkout:** Sistema soma os valores e gera um único Pix Copia e Cola (Mercado Pago).
5. **Confirmação:** O Webhook recebe a aprovação e dispara o comando de hardware.
6. **Entrega:** A máquina gira as molas correspondentes sequencialmente.

## Gestão de Estoque
- Cada "mola" (coordenada) tem uma capacidade máxima e um saldo atual.
- O sistema deve subtrair do banco de dados apenas **após** a confirmação do pagamento.
- Se um item chegar a zero, ele deve ser desabilitado automaticamente na interface.

## Regras de Negócio
- **Sem Cadastro:** Foco em fricção zero. O e-mail do pagador é coletado via API do Mercado Pago.
- **Pagamento Multi-item:** Um único pagamento pode acionar múltiplos motores.