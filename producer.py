import json

import structlog
from kafka import KafkaProducer

logger = structlog.get_logger()


def on_send_success(record_metadata):
    logger.info(
        f"Message sent to {record_metadata.topic} partition "
        "{record_metadata.partition} offset {record_metadata.offset}"
    )


def on_send_error(excp):
    logger.error("Error", exc_info=excp)


def main():
    producer = KafkaProducer(
        bootstrap_servers=["localhost:9093"],
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )
    topic = "numbertopic"

    for number in range(1, 100_101):
        logger.info(f"Sending number {number}...")
        future = producer.send(topic, value=number)
        future.add_callback(on_send_success)
        future.add_errback(on_send_error)
        producer.flush()

    logger.info("All messages sent")


if __name__ == "__main__":
    main()
