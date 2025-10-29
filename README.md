# TDE 03 - Detecção de Fraude com Apache Kafka

## 🎯 Objetivo
Simular um sistema de detecção de fraudes utilizando o Apache Kafka para o envio e consumo de transações financeiras.

## 🧩 Estrutura
- **Producer**: Gera transações simuladas a cada 3 segundos e envia para o Kafka.
- **Consumer**: Lê as transações, aplica regras de fraude e salva no banco de dados.
- **Banco de Dados**: Armazena todas as transações e o resultado da análise.

## ⚙️ Regras de Fraude
1. **ALTO_VALOR** → valor ≥ 10.000  
2. **TEMPO_60s** → mesmo cliente com 4 transações em menos de 60 segundos  
3. **GEO_10m** → mesmo cliente com 2 transações em cidades diferentes em menos de 10 minutos  
