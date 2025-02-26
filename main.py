import hazelcast

client = hazelcast.HazelcastClient(
    cluster_members=[
        "127.0.0.1:5701",
        "127.0.0.1:5702",
        "127.0.0.1:5703"
    ]
)

print("Connected to Hazelcast cluster!")

client.shutdown()