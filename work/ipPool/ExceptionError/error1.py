class error1(Exception):
    def __init__(self, status_code):
        self.status_code = status_code

    def __str__(self):
        print("请求返回的状态码异常：", self.status_code)
