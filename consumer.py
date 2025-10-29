from kafka import KafkaConsumer
import json, sqlite3
from datetime import datetime

consumer = KafkaConsumer('transacoes',
                         bootstrap_servers='localhost:9092',
                         value_deserializer=lambda v: json.loads(v.decode('utf-8')))

conn = sqlite3.connect('transacoes.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS transacoes
    (id TEXT, cliente_id TEXT, valor REAL, cidade TEXT, data_hora TEXT, fraude TEXT)''')

historico = []

for msg in consumer:
    t = msg.value
    t['data_hora'] = datetime.fromisoformat(t['data_hora'])
    fraude = None

    if t['valor'] >= 10000:
        fraude = "ALTO_VALOR"

    ultimas = [x for x in historico if x['cliente_id'] == t['cliente_id'] and (t['data_hora'] - x['data_hora']).total_seconds() < 60]
    if len(ultimas) >= 3:
        fraude = "TEMPO_60s"

    ultimas_geo = [x for x in historico if x['cliente_id'] == t['cliente_id'] and (t['data_hora'] - x['data_hora']).total_seconds() < 600]
    cidades = {x['cidade'] for x in ultimas_geo}
    cidades.add(t['cidade'])
    if len(cidades) > 1:
        fraude = "GEO_10m"

    historico.append(t)
    cursor.execute("INSERT INTO transacoes VALUES (?, ?, ?, ?, ?, ?)",
                   (t['id'], t['cliente_id'], t['valor'], t['cidade'], t['data_hora'].isoformat(), fraude))
    conn.commit()

    if fraude:
        print(f" FRAUDE {fraude}: {t}")
    else:
        print(f"Transação OK: {t}")
