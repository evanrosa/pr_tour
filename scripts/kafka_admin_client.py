from kafka.admin import KafkaAdminClient, NewTopic
import json

with open("topics_config.json", "r") as f:
    topics_config = json.load(f)

admin_client = KafkaAdminClient(
    bootstrap_servers="kafka:9093",
    client_id="topic_creator"
)

new_topics = [
    NewTopic(
        name=topic["name"],
        num_partitions=topic["num_partitions"],
        replication_factor=topic["replication_factor"],
    )
    for topic in topics_config
]

try:
    # This will create the topics if they do not exist.
    admin_client.create_topics(new_topics=new_topics, validate_only=False)
    print("Topics available:", admin_client.list_topics())
    print("Topics created successfully")
except Exception as e:
    print(f"Error creating topics: {e}")
