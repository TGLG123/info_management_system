import threading

_thread_locals = threading.local()

def set_current_request(request):
    """存储当前请求对象"""
    print(f"Setting request: {request}")  # 调试输出：设置请求对象
    _thread_locals.request = request

def get_current_request():
    """获取当前线程存储的请求对象"""
    current_request = getattr(_thread_locals, 'request', None)
    print(f"Getting current request: {current_request}")  # 调试输出：获取请求对象
    return current_request

def clear_request():
    """清除当前线程存储的请求对象"""
    print(f"Clearing request: {_thread_locals.__dict__.get('request', None)}")  # 调试输出：清理前的请求对象
    _thread_locals.request = None
    print("Request cleared.")  # 调试输出：清理完成

class RequestMiddleware:
    """中间件：将请求存储到线程安全的存储中"""
    def __init__(self, get_response):
        self.get_response = get_response
        print("RequestMiddleware initialized.")  # 调试输出：中间件初始化完成

    def __call__(self, request):
        print(f"Middleware called for request: {request}")  # 调试输出：中间件被调用
        set_current_request(request)  # 存储请求对象
        response = self.get_response(request)
        clear_request()  # 清理请求对象
        return response

class ThreadLocalMiddleware:
    """将 request 存储到线程本地"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        from utils.thread_local import set_current_request, clear_request

        set_current_request(request)  # 存储 request
        response = self.get_response(request)
        clear_request()  # 清理 request
        return response
