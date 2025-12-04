import threading

_thread_locals = threading.local()

def set_current_request(request):
    """将当前请求存储到线程本地"""
    _thread_locals.request = request

def get_current_request():
    """从线程本地获取当前请求"""
    return getattr(_thread_locals, 'request', None)

def clear_request():
    """清除当前线程存储的请求对象"""
    _thread_locals.request = None
