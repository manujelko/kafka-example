import json

import structlog
from kafka import KafkaConsumer

logger = structlog.get_logger()


def main():
    consumer = KafkaConsumer(
        "numbertopic",
        bootstrap_servers=["localhost:9093"],
        group_id="new-consumer-group",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="earliest",
    )

    logger.info("Consuming messages...")
    for message in consumer:
        number = message.value
        squared = number * number
        logger.info(f"Received: {number}, Squared: {squared}")


if __name__ == "__main__":
    main()
