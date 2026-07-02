import time
from cryptography.fernet import Fernet

def timer(func):
    """
    Docstring for timer - no param
    :param func: Description
    """
        
    def wrapper():
        print(f"Now start to deal {func.__name__}")
        start_time = time.time()
        res = func()
        finish_time = time.time()
        print(f"{func.__name__} is completed, calculating the cost time...")
            
        cost_time = finish_time - start_time

        print(f"Total costed {round(cost_time,2)} seconds.")
        return res
    return wrapper


def divisible_timer(divisor = 2):

    def timer(func):

        def wrapper(*args,**kwargs):
            print(f"Now start to deal {func.__name__}")
            start_time = time.time()
            res = func(*args,**kwargs)
            finish_time = time.time()
            print(f"{func.__name__} is completed, check if cost time is divisible by {divisor}")
            
            cost_time = round(finish_time - start_time,2)
            
            print(f"Total costed {cost_time} seconds.")

            if cost_time % divisor == 0:
                print(f"Could be divisible, cost time is {cost_time}")
            else:
                print(f"Could not be divised by {divisor}.")
            
            return res
        return wrapper
    return timer

default_key = Fernet.generate_key()
def encrypt_decorator(input_key = default_key):

    def decorator(func):

        def wrapper(msg):
            print(f"original message is {msg}")
            cipher = Fernet(input_key)
            encrypted = cipher.encrypt(msg.encode())
            # print(f"After encryted the message is {encrypted}")

            res = func(encrypted) # 将加密后的信息传回给func 5. 被装饰函数自动打印加密后的数据
            
            return res
        return wrapper
    return decorator

