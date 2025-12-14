# sparkk

Small PySpark examples + a Kafka streaming demo.

## What’s in here

- [generate_data.py](generate_data.py): Generates a synthetic ecommerce dataset into `sales.csv`.
- [sales.csv](sales.csv): Sample dataset used by `ecommerce.py`.
- [ecommerce.py](ecommerce.py): PySpark batch analytics over `sales.csv` (revenue by country, top products in USA, top customers by spend).
- [romeo](romeo): Text input for `wordcount.py`.
- [wordcount.py](wordcount.py): PySpark batch wordcount over `romeo`.
- [kafka_producer.py](kafka_producer.py): Streams Coinbase tickers (BTC-USD, ETH-USD) into Kafka topic `crypto-stream`.
- [spark_kafka.py](spark_kafka.py): PySpark Structured Streaming job reading `crypto-stream` and printing windowed average prices.

## Prerequisites

- Linux/macOS recommended
- Python 3.10+ (this repo works with Python 3.12)
- Java (required by Spark) — e.g. OpenJDK 11 or 17
- For the streaming demo:
  - A running Kafka broker on `localhost:9092`
  - Network access to `wss://ws-feed.exchange.coinbase.com`

## Python environment

This repo assumes a virtual environment in `.venv/`.

```bash
cd /path/to/sparkk
python3 -m venv .venv
source .venv/bin/activate

# Install deps (if not already installed)
pip install pyspark kafka-python websocket-client
```

## Run the batch examples

### 1) Generate the ecommerce dataset

```bash
./.venv/bin/python generate_data.py
```

This creates/overwrites `sales.csv` in the project root.

### 2) Run ecommerce analytics (Spark batch)

```bash
./.venv/bin/python ecommerce.py
```

### 3) Run wordcount (Spark batch)

```bash
./.venv/bin/python wordcount.py
```

## Run the Kafka + Spark streaming demo

### Step 0: Start Kafka

You need a Kafka broker reachable at `localhost:9092`.

If you already have Kafka installed locally, start it the way you normally do.

If you prefer Docker, here’s a common single-node setup (Kafka “KRaft” mode):

```bash
docker run --name kafka -p 9092:9092 -d \
  -e KAFKA_CFG_NODE_ID=1 \
  -e KAFKA_CFG_PROCESS_ROLES=broker,controller \
  -e KAFKA_CFG_CONTROLLER_QUORUM_VOTERS=1@127.0.0.1:9093 \
  -e KAFKA_CFG_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093 \
  -e KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 \
  -e KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=PLAINTEXT:PLAINTEXT,CONTROLLER:PLAINTEXT \
  -e KAFKA_CFG_CONTROLLER_LISTENER_NAMES=CONTROLLER \
  -e KAFKA_CFG_INTER_BROKER_LISTENER_NAME=PLAINTEXT \
  bitnami/kafka:latest
```

### Step 1: Create the topic

Create the Kafka topic `crypto-stream` (once):

```bash
# If using the Bitnami Docker container above:
docker exec -it kafka kafka-topics.sh --bootstrap-server localhost:9092 \
  --create --if-not-exists --topic crypto-stream --partitions 1 --replication-factor 1
```

### Step 2: Start the producer (websocket → Kafka)

```bash
./.venv/bin/python kafka_producer.py
```

You should see logs like “Sent to Kafka: …”.

### Step 3: Start the Spark streaming consumer (Kafka → Spark)

In a second terminal:

```bash
./.venv/bin/python spark_kafka.py
```

You should see 10-second window aggregates printed to the console (average price per symbol).

## Troubleshooting

- **`ModuleNotFoundError: pyspark`**: Ensure you’re using the venv interpreter `./.venv/bin/python` and ran `pip install pyspark`.
- **Spark fails to start**: Install Java (OpenJDK 11/17) and ensure `java -version` works.
- **Kafka connection errors**: Confirm Kafka is reachable at `localhost:9092` and the topic `crypto-stream` exists.
- **No data in Spark**: Ensure `kafka_producer.py` is running and your network can access Coinbase websocket.
