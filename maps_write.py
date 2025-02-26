
import hazelcast

client = hazelcast.HazelcastClient(
    cluster_name="dev",
    cluster_members=[
        "127.0.0.1:5701",
        "127.0.0.1:5702",
        "127.0.0.1:5703"
    ]
)

numbers = client.get_map("map").blocking()

for i in range(1000):
    numbers.put(i, "Value of" + str(i))

print("Distributed maps success!")

client.shutdown()

