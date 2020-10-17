import threading
from concurrent.futures import ThreadPoolExecutor as ThreadPool


# philosopher 哲学家的编号。
# pickLeftFork 和 pickRightFork 表示拿起左边或右边的叉子。
# eat 表示吃面。
# putLeftFork 和 putRightFork 表示放下左边或右边的叉子。
class DiningPhilosophers:
    def __init__(self, num, left_fork, right_fork):
        self.num = num
        self.left_fork = left_fork
        self.right_fork = right_fork

    def pickLeftFork(self):
        self.left_fork.acquire()
        print([self.num, 1, 1])

    def pickRightFork(self):
        self.right_fork.acquire()
        print([self.num, 2, 1])

    def eat(self):
        print([self.num, 0, 3])

    def putLeftFork(self):
        self.left_fork.release()
        print([self.num, 1, 0])

    def putRightFork(self):
        self.right_fork.release()
        print([self.num, 2, 0])

    def wantsToEat(self):
        self.pickLeftFork()
        self.pickRightFork()
        self.eat()
        self.putRightFork()
        self.putLeftFork()

# philosopher_count思想家的数量
# eat_count 吃的次数
# 思想家编号=1
# 则左边的叉子编号为1 右边的叉子编号为2
def begin(philosopher_count, eat_count):
    forks = []
    for _ in range(philosopher_count):
        forks.append(threading.Lock())

    philosophers = []
    for num in range(philosopher_count):
        left_fork = forks[num]
        if num == philosopher_count - 1:
            right_fork = forks[0]
        else:
            right_fork = forks[num + 1]
        philosophers.append(DiningPhilosophers(num, left_fork, right_fork))

    pool = ThreadPool(max_workers=philosopher_count)
    for _ in range(eat_count):
        for philosopher in philosophers:
            pool.submit(philosopher.wantsToEat(), philosopher)
    pool.shutdown()

begin(5,1)
