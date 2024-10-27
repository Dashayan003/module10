import threading
import random
from time import sleep
from threading import Lock


class Bank(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.balance = 0
        self.lock = Lock()

    def deposit(self):
        for i in range(100):
            numb = random.randint(50, 500)
            self.balance += numb
            print(f"Пополнение: {numb}. Баланс: {self.balance}")
            if self.balance >= 500 and self.lock.locked():
                self.lock.release()
            sleep(0.001)

    def take(self):
        for i in range(100):
            numb = random.randint(50, 500)
            print(f"Запрос на {numb}")
            if numb <= self.balance:
                self.balance -= numb
                print(f"Снятие: {numb}. Баланс: {self.balance}")
            else:
                print("Запрос отклонён, недостаточно средств")
                self.lock.acquire()


bk = Bank()

th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()

th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')
