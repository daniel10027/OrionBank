"""
Fichier kafka.py
----------------
Ce module centralise la configuration et les utilitaires pour Kafka.

Fonctionnalités :
- Initialisation d'un Producer Kafka
- Initialisation d'un Consumer Kafka
- Envoi et lecture de messages
- Gestion des erreurs et reconnexion automatique

Librairie utilisée : confluent-kafka (plus performante que kafka-python)
Installation : pip install confluent-kafka
"""

import json
import logging
from confluent_kafka import Producer, Consumer, KafkaError

logger = logging.getLogger(__name__)

# Configuration de base (peut être déplacée dans settings.py)
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
KAFKA_GROUP_ID = "backoffice-group"
KAFKA_AUTO_OFFSET_RESET = "earliest"


# === Producer Kafka ===
def get_kafka_producer():
    """Retourne un Producer Kafka configuré."""
    conf = {"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS}
    return Producer(conf)


def send_kafka_message(topic: str, key: str, value: dict):
    """
    Envoie un message JSON dans un topic Kafka.
    :param topic: Nom du topic Kafka
    :param key: Clé du message
    :param value: Valeur (dict) qui sera transformée en JSON
    """
    try:
        producer = get_kafka_producer()
        producer.produce(
            topic,
            key=str(key),
            value=json.dumps(value).encode("utf-8"),
        )
        producer.flush()
        logger.info(f"[Kafka] Message envoyé sur {topic} | key={key} | value={value}")
    except Exception as e:
        logger.error(f"[Kafka] Erreur lors de l'envoi sur {topic} : {e}")


# === Consumer Kafka ===
def get_kafka_consumer(topics: list[str]):
    """
    Initialise un Consumer Kafka abonné à une liste de topics.
    :param topics: Liste des topics
    """
    conf = {
        "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
        "group.id": KAFKA_GROUP_ID,
        "auto.offset.reset": KAFKA_AUTO_OFFSET_RESET,
    }
    consumer = Consumer(conf)
    consumer.subscribe(topics)
    return consumer


def consume_kafka_messages(topics: list[str], callback):
    """
    Consomme en boucle des messages Kafka et appelle un callback.
    :param topics: Liste des topics
    :param callback: Fonction callback(message: dict)
    """
    consumer = get_kafka_consumer(topics)
    logger.info(f"[Kafka] Abonné aux topics : {topics}")

    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() != KafkaError._PARTITION_EOF:
                    logger.error(f"[Kafka] Erreur consumer : {msg.error()}")
                continue

            try:
                data = json.loads(msg.value().decode("utf-8"))
                logger.info(f"[Kafka] Message reçu : {data}")
                callback(data)
            except Exception as e:
                logger.error(f"[Kafka] Erreur parsing message : {e}")
    except KeyboardInterrupt:
        logger.info("[Kafka] Arrêt consumer")
    finally:
        consumer.close()
