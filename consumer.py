import asyncio
import json

import structlog
from aiokafka import AIOKafkaConsumer

logger = structlog.get_logger()


async def consume() -> None:
    consumer = AIOKafkaConsumer(
        "numbertopic",
        bootstrap_servers=["localhost:9093"],
        group_id="new-consumer-group",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="earliest",
    )
    # Get cluster layout and join group `new-consumer-group`
    await consumer.start()
    try:
        logger.info("Consuming messages...")
        async for message in consumer:
            number = message.value
            squared = number * number
            logger.info(f"Received: {number}, Squared: {squared}")
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(consume())
