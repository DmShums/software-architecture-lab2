import hazelcast
import multiprocessing

def update_map():
    # Each process must have its own client
    client = hazelcast.HazelcastClient()
    numbers = client.get_map("map").blocking()

    for _ in range(10000):
        value = numbers.get("key")
        numbers.put("key", value + 1)

    client.shutdown()
    print("Process finished updating map.")

if __name__ == "__main__":
    client = hazelcast.HazelcastClient()
    numbers = client.get_map("map").blocking()

    numbers.put_if_absent("key", 0)

    processes = []
    for _ in range(3):
        p = multiprocessing.Process(target=update_map)
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    final_value = numbers.get("key")
    print(f"Final value: {final_value}")

    client.shutdown()