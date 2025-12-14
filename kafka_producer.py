import websocket
import json
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers = ['localhost:9092'])

def on_open(ws):

    print("--- Connection opened ---")
    sub = {
        "type": "subscribe",
        "product_ids": ["BTC-USD", "ETH-USD"],
        "channels": ["ticker"]
    }

    ws.send(json.dumps(sub))


def on_message(ws, message):
    data = json.loads(message)

    if data.get("type") == "ticker":
        record =  {
            'time': data.get('time'),
            'symbol': data.get('product_id'),
            'price': float(data.get('price')),
        }

    producer.send('crypto-stream', json.dumps(record).encode('utf-8'))
    
    print(f'Sent to Kafka: {record}')


def on_error(ws, err):
    print(f'Error: {err}')

socket_url = 'wss://ws-feed.exchange.coinbase.com'
ws = websocket.WebSocketApp(socket_url,
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error)

try:
    ws.run_forever()
except KeyboardInterrupt:
    print("Exiting...")