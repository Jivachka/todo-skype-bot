from threading import Thread

from class_works import SkypeFileManager
from data import login_name, password


# Start multiple threads
def run_main_loop():
    while True:
        pass

file_manager = SkypeFileManager(login_name, password)

num_threads = 5
threads = [Thread(target=file_manager.start_thread) for _ in range(num_threads - 1)]
threads.append(Thread(target=file_manager.start_thread())) # 1st thread
threads.append(Thread(target=run_main_loop)) # 2 thread
for t in threads:
    t.start()

for t in threads:
    t.join()
