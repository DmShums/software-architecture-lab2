import hazelcast
import threading
import time

def producer(client: hazelcast.HazelcastClient, map_name):
    my_queue = client.get_queue(map_name).blocking()
    
    for i in range(1, 101):
        try:
            if my_queue.remaining_capacity() > 0:
                my_queue.put(i)
                print(f"Produced: {i}")
            else:
                print(f"Queue is full, unable to produce: {i}")
        except Exception as e:
            print(f"Producer failed to put item: {e}")
        time.sleep(0.1)

def consumer(client: hazelcast.HazelcastClient, map_name):
    my_queue = client.get_queue(map_name).blocking()
    
    while True:
        value = my_queue.take()
        print(f"Consumed: {value}")
        time.sleep(0.1)

if __name__ == "__main__":
    time_start = time.time()

    client1 = hazelcast.HazelcastClient()
    client2 = hazelcast.HazelcastClient()
    client3 = hazelcast.HazelcastClient()

    map_name = "default"

    client1.get_queue(map_name).blocking()

    producer_thread = threading.Thread(target=producer, args=(client1, map_name))
    producer_thread.start()

    consumer_thread1 = threading.Thread(target=consumer, args=(client2, map_name))
    consumer_thread2 = threading.Thread(target=consumer, args=(client3, map_name))
    consumer_thread1.start()
    consumer_thread2.start()

    producer_thread.join()
    consumer_thread1.join()
    consumer_thread2.join()

    client1.shutdown()
    client2.shutdown()
    client3.shutdown()

    time_end = time.time()
    print(f"Time taken: {time_end - time_start} seconds.")