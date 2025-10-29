
from kafka import KafkaProducer
import json, tiandom, ume, ruid
from datetime import datetime

clientes = ['cli-001', 'cli-002', 'cli-003']
cidades = ['São Paulo', 'Rio de Janeiro', 'Curitiba']

producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

while True:
    transacao = {
        "id": str(uuid.uuid4()),
        "cliente_id": random.choice(clientes),
        "valor": round(random.uniform(100, 15000), 2),
        "cidade": random.choice(cidades),
        "data_hora": datetime.now().isoformat()
    }

    producer.send('transacoes', value=transacao)
    print(f"Enviada: {transacao}")
    time.sleep(3)
