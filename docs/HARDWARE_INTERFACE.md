# Protocolo de Comunicação Hardware/Software

## Arquitetura de Comunicação
O Backend falará com o ESP32 via protocolo **MQTT** (Message Queuing Telemetry Transport).

## Formato da Mensagem (JSON)
Quando o pagamento for aprovado, o Backend publicará no tópico `vending/dispense`:

```json
{
  "transaction_id": "153718375671",
  "actions": [
    {"motor": "A1", "quantity": 2, "time_ms": 2500},
    {"motor": "E3", "quantity": 1, "time_ms": 2500}
  ]
}