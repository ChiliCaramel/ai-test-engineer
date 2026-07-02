"""
记得要注册到settings.py - MIDDLEWARE中
"""

import time

class RequestLoggerMiddleware:
    """
    get_response 是一个回调函数，是处理请求的核心方法，执行请求-响应的完整过程，是django框架原生的处理请求方法
    get_response 执行时必须传递一个request 请求对象
    """

    def __init__(self,get_response):
        # get_response 类似于装饰器的被装饰函数
        self.get_response = get_response
    
    def __call__(self,request):
        # 处理请求前的逻辑
        start_time = time.time()
        response = self.get_response(request)

        # 处理响应后的逻辑
        end_time = time.time()
        elapsed_time = end_time - start_time

        # 记录请求路径和处理时间
        self.log_request(request.path,elapsed_time)

        return response
    
    def log_request(self,path,elapsed_time):
        # 可以写日志输出到文件、数据库等任何地方
        print(f"Request to {path} took {elapsed_time:.2f} secs.")
