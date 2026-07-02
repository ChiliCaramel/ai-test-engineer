from django.http import HttpResponse
from django.utils import timezone
from pracdjango.models import IPRequestLog



def rate_limit(requests_per_day=3):
    
    def my_decorate(view_func):
        def wrapper(request,*args,**kwargs):
            ip_addr = request.META.get('REMOTE_ADDR')
            today = timezone.now().date()

            log , created = IPRequestLog.objects.get_or_create(
                ip_address = ip_addr,
                last_request_time__date = today,
                defaults = {'request_count':1,'last_request_time':timezone.now()}
            )

            # 判断是否已经有条目，如果已经有了则更新count 和 last_request_time
            if not created:
                if log.request_count >= requests_per_day:
                    return HttpResponse('Too Many Requests',status = 429)
                log.request_count +=1
            log.last_request_time = timezone.now()
            log.save()

            return view_func(request, *args, **kwargs)
        return wrapper
    return my_decorate

"""

这里已经有return了 为什么 超出限制以后还是会优先present 装饰器返回的结果
这里不是"两个 return 谁优先"的问题，而是：超限的时候，requests_ip_addr 函数体里的 return JsonResponse(...) 根本没有被执行过。

关键是要理解：加了 @rate_limit(...) 之后，外面（包括 Django 路由）实际调用的已经不是你写的那个 requests_ip_addr 函数本体了，而是 wrapper。等价于这样展开：


def requests_ip_addr(request):
    return JsonResponse({'msg':'ok'}, status=200)

requests_ip_addr = rate_limit(requests_per_day=4)(requests_ip_addr)
跑完这一行赋值之后，模块里名字 requests_ip_addr 指向的已经是 wrapper 这个新函数，你原来写的那个函数体被存进了 wrapper 内部的闭包变量 view_func 里，只有 wrapper 主动调用 view_func(...) 的时候，它才会执行。

所以实际调用流程是这样的：


def wrapper(request, *args, **kwargs):
    ...查表...
    if 超限:
        return HttpResponse('Too Many Requests', status=429)
        # ↑ 函数在这里就直接结束、返回了
        # view_func(request, ...) 这一行根本没机会被跑到
    ...
    return view_func(request, *args, **kwargs)
    # ↑ 只有走到这里，才会真正调用你写的 requests_ip_addr 函数体，
    #   它内部的 return JsonResponse(...) 才会执行，
    #   执行完的结果再被这个 return 原样传出去
超限那个分支一旦 return，整个 wrapper 函数当场结束，view_func(request, *args, **kwargs) 这一行代码完全不会被执行——不是"两个 return 谁先谁后/谁优先"，而是后面那行代码压根没机会运行。这也正是装饰器模式的核心用法：外层函数可以决定"要不要、什么时候"去调用被装饰的原函数，从而拦截/短路它的执行。
"""

