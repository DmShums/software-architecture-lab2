import hazelcast
import threading
import time

def update_map(client, client_name):
    numbers = client.get_map("numbers").blocking()
    numbers.put_if_absent("key", 0)

    for _ in range(10000):
        numbers.lock("key")
        try:
            value = numbers.get("key")
            numbers.put("key", value + 1)
        finally:
            numbers.unlock("key")

    print(f"{client_name} finished updating map.")

if __name__ == "__main__":
    time_start = time.time()

    clients = []
    for i in range(3):
        clients.append(hazelcast.HazelcastClient())

    threads = []
    for i in range(3):
        t = threading.Thread(target=update_map, args=(clients[i], f"numbers{i}"))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    numbers = clients[0].get_map("numbers").blocking()
    final_value = numbers.get("key")
    print(f"Final value: {final_value}")

    for i in range(3):
        clients[i].shutdown()

    time_end = time.time()
    print(f"Time taken: {time_end - time_start} seconds.")