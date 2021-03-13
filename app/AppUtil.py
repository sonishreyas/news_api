class AppUtil:
    def __init__(self):
        pass

    def get_ip(self, request):
        ip = request.remote_addr
        if 'X-Forwarded-For' in request.headers:
            proxy_data = request.headers['X-Forwarded-For']
            ip_list = proxy_data.split(',')
            ip = ip_list[0]  # first address in list is User IP
        return ip