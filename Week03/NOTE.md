# python第三周

主要内容：多进程&多线程

1. 多进程如何创建 multiprocessing.Process
2. 多进程数据如何共享：队列、pipe、共享内存
3. 如何解决多人写入共享数据时的安全问题：锁机制
4. 多任务除了多进程，还有多线程和协程。
5. 多线程的锁机制



## 一. 进程

API：

- 获取进程编号os.getppid()



### 进程通信

进程通信的三种方式

- 队列
- 管道
- 共享内存



#### 1. 队列

- get()     最早put的值。
  <img src="/Users/happybangs/Library/Application Support/typora-user-images/image-20201018005237676.png" alt="image-20201018005237676" style="zoom:50%;" />

  block + timeout可以配合出现。

  block为true可以阻塞当前进程直到读取到数据，或者超时抛出queue.Empty对象。

  block为false，不阻塞，为空抛出queue.Empty, timeout也没意义

- put(value)  put也有block和timeout两个参数。

  <img src="/Users/happybangs/Library/Application Support/typora-user-images/image-20201018005252680.png" alt="image-20201018005252680" style="zoom:50%;" />

  put常见的异常是queue.Full。队列满了的异常



#### 2. 管道

QUeue的底层就是管道实现的，在其基础上加了线程安全和便捷api

- 管道是双工的，两端都可以插入和进入

- 主要api

- - recv() 
  - send() 插入
  - parent_conn,      child_conn表示管道两端

- 因为多对象读写会容易有问题，所以仍然推荐队列
  <img src="/Users/happybangs/Library/Application Support/typora-user-images/image-20201018005411008.png" alt="image-20201018005411008" style="zoom:50%;" />



#### 3. 共享内存

更像单线程的写法，模拟C的共享内存方式。

- i和d表述数据类型。类似编译型的语言，需要提前申请内存，因此需要指定类型

- - string类型要引入ctypes
    <img src="/Users/happybangs/Library/Application Support/typora-user-images/image-20201018005435981.png" alt="image-20201018005435981" style="zoom:50%;" />

* 获取Value的值要使用.value
* a[:]冒号返回所有数组中的值
  <img src="/Users/happybangs/Library/Application Support/typora-user-images/image-20201018005514873.png" alt="image-20201018005514873" style="zoom:50%;" />

三种形式：队列、pipe、共享内存，队列是最通用的



### 进程锁

#### 为什么要锁？

不加锁时候，多进程是交替执行的，哪个cpu核心更空闲，则让哪一个进程去运行。

<img src="/Users/happybangs/Library/Application Support/typora-user-images/image-20201018005617200.png" alt="image-20201018005617200" style="zoom:50%;" />

不加锁带来的问题：

- p1和p2抢占同一个变量v，导致最终输出的结果不稳定。
  因为运行时拿到的value是不可预测的



#### 进程锁

`l = multiprocessing.Lock()`

- l.acquire() 锁住
- l.release() 释放

<img src="/Users/happybangs/Library/Application Support/typora-user-images/image-20201018005719066.png" alt="image-20201018005719066" style="zoom:50%;" />

代码解释：

- 除了共享变量，print也是进程不安全，需要加一把锁。打印可能会错行 （不太懂为什么会错行）
- 另外，日志内容也是不稳定的，可能无法打印（因为多进程中的日志需要达到一定数量才会打印）。此时需要加上flush



#### 死锁

<img src="/Users/happybangs/Library/Application Support/typora-user-images/image-20201018010236927.png" alt="image-20201018010236927" style="zoom:50%;" />

**join之后还对队列进行了操作，导致join没等到子进程结束，所以造成了死锁**



### 进程池

每个进程需要消耗一个逻辑上的cpu，如果进程数量大于逻辑上的cpu数量反而会进程下降。理想状态是：进程数量刚好=CPU逻辑核心的数量。

为了控制进程数量，此处因此引入了进程池：

<img src="/Users/happybangs/Library/Application Support/typora-user-images/image-20201018005845788.png" alt="image-20201018005845788" style="zoom:50%;" />



流程：

- p = Pool(4) 控制并行数量

- p.apply_async(run,     args=(i,))表示异步运行创建.

- - 注意args是元祖的形式 
  - 若使用的是p.apply(run, args) 同步方式，则会每个进程轮着执行，完全没有多进程的意义。



技巧：

- `random.choice([1,4,9,2]) `    表示人选数组中的其一
  这个随机休眠时间可以错峰，更像个人行为。比如防止某时间点同时去爬别人网站，容易触发反爬虫机制
- `os.getpid() ` 获取当前进程的id



注意事项:

- close()     也叫“温柔地结束进程”

- - 因为当你并发的进程中还有任务执行时，close会等待任务结束后再执行
  - 如果我们用的是进程池，在调用join()之前必须要先close()或者terminate()，并且在close()之后不能再继续往进程池添加新的进程

- join()：进程池对象调用join，会等待进程池中所有的子进程结束完毕再去结束父进程。 —— （me：相对于父进程来说，子进程整体的执行过程变成了同步的）

- - 父进程一般需要等到拿到所有子进程结果后，所以需要用到join

- terminate()：一旦运行到此步，不管任务是否完成，立即终止

- 进程池不一定按照创建时候的顺序执行。你可以使用队列来保证顺序



#### 1. Pool的扩展1：timeout

<img src="/Users/happybangs/Library/Application Support/typora-user-images/image-20201018010123360.png" alt="image-20201018010123360" style="zoom:50%;" />

- *超时的错误**：**raises     multiprocessing.TimeoutError*

- *使用get可以设置超时时间*



#### Pool的扩展2：map 快速创建进程池

<img src="/Users/happybangs/Library/Application Support/typora-user-images/image-20201018010159936.png" alt="image-20201018010159936" style="zoom:50%;" />

1.使用with描述符更方便

2.pool.map 输出的是列表

- 第一个参数fn
- 第二个参数是fn的参数，只接受一个fn的参数。如果需要可以将参数转换为元组或者列表

3.pool.imap 输出的是迭代器

- 使用next拿到最近的一个，支持timeout





## 线程

[python doc](https://docs.python.org/zh-cn/3.7/library/threading.html)

<img src="/Users/happybangs/Library/Application Support/typora-user-images/image-20201018010359474.png" alt="image-20201018010359474" style="zoom:50%;" />

1. 进程和线程的区别：
   多进程并发会有很重的资源开销。
   多线程之间同步数据更方便，线程之间的数据是共享的。

2. 阻塞和非阻塞是从调用方的角度定义的。对调用方来说是阻塞的还是不阻塞的。

   * request是阻塞的

   * scrapy是非阻塞的

3. 同步和异步是被调用方（接收方）的角度。
    所以（异）同步和（非）阻塞会同时出现。
   PS：打电话的例子没完全太懂...

   > *#* *调用方*
   >
   > *#* *阻塞 得到调用结果之前，线程会被挂起*
   >
   > *#* *非阻塞 不能立即得到结果，不会阻塞线程*
   >
   > *#* *被调用方* 
   >
   > *#* *同步 得到结果之前，调用不会返回*
   >
   > *#* *异步 请求发出后，调用立即返回，没有返回结果，通过回调函数得到实际结果*

4. 多进程用于占用计算机cpu，更多的利用资源；多线程用于更方便的通信。

5. 多进程和多线程的调度都是有系统来调度（切换等）的。
   如果希望用户能把控进程或者线程的切换，就需要“协程”。

6. 并发和并行。
   两个咖啡表示两个cpu核心。
   第一张为并发，交替使用。（基于线程的并行）
   第二张是并行（多进程）
   <img src="/Users/happybangs/Library/Application Support/typora-user-images/image-20201018010700116.png" alt="image-20201018010700116" style="zoom:50%;" />



### 1. 线程的创建

和进程的创建很类似：

<img src="/Users/happybangs/Library/Application Support/typora-user-images/image-20201018010730328.png" alt="image-20201018010730328" style="zoom:50%;" />

1. 函数方式

   ```python
   import threading
   # 这个函数名可随便定义
   def run(n):
     print("current task：", n)
   if __name__ == "__main__":
       t1 = threading.Thread(target=run, args=("thread 1",))
       t2 = threading.Thread(target=run, args=("thread 2",))
       t1.start()
       t2.start()
   ```

2. 类方式

   ```python
   class MyThread(threading.Thread):
   	def __init__(self, n):
   	super().__init__() # 重构run函数必须要写
   	self.n = n
   	def run(self): # 覆盖父类定义的run方法
   	print("current task：", self.n)
   	if __name__ == "__main__":
   	t1 = MyThread("thread 1")
   	t2 = MyThread("thread 2")
   	t1.start()
   	t2.start()
   	# 将 t1 和 t2 加入到主线程中
   	t1.join()
   t2.join()
   ```

3. 调试技巧
   * thread.is_alive() 用于判断线程是否是活动的，返回布尔值 



### 2. 线程安全

 解决方法也是锁：

* 普通锁：lock,rlock（可嵌套）

* 高级锁：信号量(liang 四声)、事件锁、条件锁



#### 普通锁

`threading.lock()`

<img src="/Users/happybangs/Library/Application Support/typora-user-images/image-20201018011259810.png" alt="image-20201018011259810" style="zoom:50%;" />

#### Rlock

可嵌套
<img src="/Users/happybangs/Library/Application Support/typora-user-images/image-20201018011248794.png" alt="image-20201018011248794" style="zoom:50%;" />



#### 条件锁

满足某个条件才释放锁，比如生产者消费者模式.
`threading.Condition()`。
线程的构造函数需要把条件锁带到args中

<img src="/Users/happybangs/Library/Application Support/typora-user-images/image-20201018011234550.png" alt="image-20201018011234550" style="zoom:50%;" />

#### 信号量

最多允许多少个线程同时运行

 `semaphore = threading.BoundedSemaphore(5) `*#* *最多允许**5**个线程同时运行**

#### 事件锁

<img src="/Users/happybangs/Library/Application Support/typora-user-images/image-20201018011220289.png" alt="image-20201018011220289" style="zoom:50%;" />

#### 定时器

```python
	# 定时器： 指定n秒后执行
from threading import Timer
def hello():
		print("hello, world")
t = Timer(1,hello) # 表示1秒后执行hello函数
t.start()
```



总结：主要需要掌握普通锁，嵌套时用RLock

 

### 3. 线程中的队列

线程的数据是可以共享的，所以队列不是线程数据通信的主要工具，但他是一个非常重要的数据结构。

介绍了队列常见的API

- queue.put()
- queue.get()
- queue.taskdone()     用于提示q.join()是是否停止阻塞，让线程继续执行/退出



队列的类型：

1. 优先级队列：queue.PriorityQueue()

   q.put((1,"work"))

   q.put((-1,"life")) 

   > *#* *每个元素都是元组*
   >
   > *#* *数字越小优先级越高**，优先级越高越优先被取出来*
   >
   > *#* *同优先级先进先出*



2.  后进先出队列（堆栈） `*queue.LifoQueue* `
3. 双向队列 `q.deque` 不常用不做太多介绍

 

### 4. 用条件锁实现生产者和消费者模式（例子）：

```python
import queue
q = queue.Queue(5)
q.put(111)        # 存队列
q.put(222)
q.put(333)
 
print(q.get())    # 取队列
print(q.get())
q.task_done()     # 每次从queue中get一个数据之后，当处理好相关问题，最后调用该方法，
                  # 以提示q.join()是否停止阻塞，让线程继续执行或者退出
print(q.qsize())  # 队列中元素的个数， 队列的大小
print(q.empty())  # 队列是否为空
print(q.full())   # 队列是否满了

###############

import queue
import threading
import random
import time

writelock = threading.Lock()

class Producer(threading.Thread):
    def __init__(self, q, con, name):
        super(Producer, self).__init__()
        self.q = q
        self.name = name
        self.con =con
        print(f'Producer {self.name} Started')
    
    def run(self):
        while 1: # 实现永久循环
            global writelock
            print('in producer1' + self.name)
            self.con.acquire()  # 获得锁对象
            print('in producer2' + self.name)
            if self.q.full():   # 队列满
                with writelock:
                    print('Queue is full , producer wait')
                self.con.wait()  # 等待资源， 该线程不挂起，直到被notify再重新执行
            
            else:
                value = random.randint(0,10)
                with  writelock:
                    print(f'{self.name} put value {self.name} {str(value)} in queue')
                self.q.put( (f'{self.name} : {str(value)}') ) # 放入队列
                self.con.notify()   # 通知消费者
                time.sleep(1)
        self.con.release()


class Consumer(threading.Thread):
    def __init__(self, q, con, name):
        super(Consumer, self).__init__()
        self.q = q
        self.name = name
        self.con =con
        print(f'Consumer {self.name} Started')

    def run(self):
        while 1:
            global writelock
            print('in consumer' + self.name)    
            self.con.acquire()
            print('in consumer2' + self.name)    
            if self.q.empty():   # 队列空
                with writelock:
                    print('Queue is empty , consumer wait')
                self.con.wait()  # 等待资源
            else:
                value = self.q.get()
                with writelock:
                    print(f'{self.name} get value {value} from queue')              
                self.con.notify()   # 通知生产者
                time.sleep(1)
        self.con.release()



if __name__ == '__main__':
    q = queue.Queue(10)
    con = threading.Condition()   # 条件变量锁

    p1 = Producer(q, con, 'P1')
    p1.start()
    p2 = Producer(q, con, 'P2')
    p2.start()
    c1 = Consumer(q, con, 'C1')
    c1.start()

# 练习使用列表实现队列
```



### 5. 线程池

<img src="/Users/happybangs/Library/Application Support/typora-user-images/image-20201018011739242.png" alt="image-20201018011739242" style="zoom:50%;" />

例子：比较计算耗时较长的单进程单线程、两进程、两线程的时间：

（2线程/p18_pvt.py ）

输出：

<img src="/Users/happybangs/Library/Application Support/typora-user-images/image-20201018011755308.png" alt="image-20201018011755308" style="zoom:50%;" />

结果分析：两进程 > 多线程 > 单进程单线程

- 为什么两进程大于单进程单线程/ 2？虽然理论上一个进程应该单进程单线程只占一半时间，两进程占了两个核，进程的上下文交互时候需要占用的时间。
- 为什么多线程大于单进程单线程？cpython的多线程是伪并发的多线程，同一时间只能运行一个线程

<img src="/Users/happybangs/Library/Application Support/typora-user-images/image-20201018011820047.png" alt="image-20201018011820047" style="zoom:50%;" />

解释:

* 哪个线程拿到锁，哪个线程才可以去执行cpu
* 一旦遇到IO操作，GIL锁就会被释放，使得其他的锁可以抢夺锁的运行权限



<img src="/Users/happybangs/Library/Application Support/typora-user-images/image-20201018011841423.png" alt="image-20201018011841423" style="zoom:50%;" />

解释：

有图看到，同一时间只有一个线程拿到锁，一个线程在运行。

所以多线程的运行时间比单进程的效率还低。

对CPU密集型的开销，多线程的运行时间比单进程的效率还低（比如例子）

但IO密集型的任务，多线程会大大提升效率 （比如爬虫，等待爬取结果需要非阻塞的多线程）