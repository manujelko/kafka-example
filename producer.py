import asyncio
import json

import structlog
from aiokafka import AIOKafkaProducer

logger = structlog.get_logger()


async def send_one(producer: AIOKafkaProducer, topic: str, value: int) -> None:
    try:
        record_metadata = await producer.send_and_wait(topic, value)
        logger.info(
            "Message sent",
            topic=record_metadata.topic,
            partition=record_metadata.partition,
            offset=record_metadata.offset,
        )
    except Exception as exc:
        logger.error("Error", exc_info=exc)


async def main() -> None:
    producer = AIOKafkaProducer(
        bootstrap_servers=["localhost:9093"],
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )
    # Get cluster layout and initial topic/partition leadership information
    await producer.start()
    try:
        topic = "numbertopic"
        for number in range(1, 1000):
            logger.info(f"Sending number {number}...")
            await send_one(producer, topic, number)
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()


if __name__ == "__main__":
    asyncio.run(main())
