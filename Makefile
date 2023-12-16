.PHONY: zookeeper
zookeeper:
	docker run --rm -it --name zookeeper --network kafka-network -p 2181:2181 zookeeper

.PHONY: kafka
kafka:
	docker run --rm -it --name kafka --network kafka-network -p 9093:9093 \
		-e KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 \
		-e KAFKA_LISTENERS=PLAINTEXT://kafka:9092,PLAINTEXT_HOST://0.0.0.0:9093 \
		-e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka:9092,PLAINTEXT_HOST://localhost:9093 \
		-e KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT \
		-e KAFKA_INTER_BROKER_LISTENER_NAME=PLAINTEXT \
		-e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
		bitnami/kafka

.PHONY: akhq
akhq:
	docker run --rm -it --name akhq --network kafka-network -p 8080:8080 \
		-v $(PWD)/akhq-config.yaml:/app/application.yml \
		tchiotludo/akhq
