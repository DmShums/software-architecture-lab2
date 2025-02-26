import hazelcast
import threading
import time

def update_map(client: hazelcast.HazelcastClient, map_name):
    my_map = client.get_map(map_name).blocking()
    key = "key"
    my_map.put_if_absent(key, 0)
    
    for _ in range(10_000):
        while True:
            old_value = my_map.get(key)
            new_value = old_value + 1

            if my_map.replace_if_same(key, old_value, new_value):
                break

if __name__ == "__main__":
    time_start = time.time()

    clients = []
    for i in range(3):
        clients.append(hazelcast.HazelcastClient())

    map_name = "numbers"
    
    threads = []
    for i in range(3):
        t = threading.Thread(target=update_map, args=(clients[i], map_name))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    numbers = clients[0].get_map(map_name).blocking()
    final_value = numbers.get("key")
    print(f"Final value: {final_value}")

    for i in range(3):
        clients[i].shutdown()

    time_end = time.time()
    print(f"Time taken: {time_end - time_start} seconds.")