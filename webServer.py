import socket
from multiprocessing import Process
import re


HTML_ROOT_DIR = "./templetes"  # 表示当前路径


def handle_client(client):

    request_data = client.recv(1024)  # 接受客户端的数据
    print("接受的数据：%s" % request_data)
    request_lines = request_data.splitlines()   # 因为是get请求，所以数据需要分段
    for line in request_lines:

        print(line)

    request_start_line = request_lines[0]  # 这段："GET /index.html HTTP/1.1"

    print("*" * 10)
    print(request_start_line.decode("utf-8"))  # 解释数据，用utf-8来解释
    file_name = re.match(r"\w+ +(/[^ ]*)", request_start_line.decode("utf-8")).group(1)  # 正则提取/index.html,(/[^ ])*  提取/index.html.
    print("filename:%s" % file_name)
    if "/" == file_name:

        file_name = "/index.html"

    try:

        file = open(HTML_ROOT_DIR + file_name, "rb")  # 打开路径下的文件夹

    except IOError:

        response_start_line = "HTTP/1.1 404 Not Found\r\n"  # 处理异常
        response_headers = "Server: My server\r\n"
        response_body = "The file is not found!"

    else:

        file_data = file.read()  # 读取文件中的数据
        file.close()    # 关闭文件

        response_start_line = "HTTP/1.1 200 OK\r\n"  # 构造响应数据
        response_headers = "Server: My server\r\n"
        response_body = file_data.decode("utf-8")

    response = response_start_line + response_headers + "\r\n" + response_body
    print("response data:", response)

    client.send(bytes(response, "utf-8"))  # 发送给客户端文件中的数据
    client.close()  # 关闭客户端


if __name__ == '__main__':

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建socket实例
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # * 地址重用（很有用）
    server.bind(("127.0.0.1", 8000))  # 绑定地址
    server.listen(126)  # 开始监听

    while True:

        client, address = server.accept()  # 接受数据
        print("[%s, %s]用户已经连上" % (address[0], address[1]))
        handleClientProcess = Process(target=handle_client, args=(client,))  # 交给函数处理
        handleClientProcess.start()  # 多线程启动，避免堵塞
        server.close()   # 关闭服务器端
