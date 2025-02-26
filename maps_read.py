import hazelcast

client = hazelcast.HazelcastClient(
    cluster_name="dev",
    cluster_members=[
        "127.0.0.1:5701",
        "127.0.0.1:5702",
    ]
)

numbers = client.get_map("map").blocking()

lost_data = []
for i in range(1000):
    number = numbers.get(i)

    if number is None:
        lost_data.append(i)

print("Lost data: ", lost_data)

client.shutdown()

