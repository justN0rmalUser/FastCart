from queue import Queue
from threading import Thread
import fdb




def qget():
    while True:
        # Блокирующий вызов: ждёт, пока в очереди появится элемент
        data = DB_QUEUE.get()  # <-- Здесь поток «засыпает», пока нет данных
        
        try:
            # 3. Обрабатываем данные (пишем в БД)
            save_to_db(data)
            print(f"✅ Обработано: {data}")
        finally:
            # 4. Говорим: «элемент обработан, можно брать следующий»
            DB_QUEUE.task_done()

def qput(jsonData):
    DB_QUEUE.put(jsonData)

