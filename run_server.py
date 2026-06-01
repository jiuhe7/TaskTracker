
"""
TaskTracker 启动脚本

用法:
    python run_server.py          # 启动在 8000 端口
    python run_server.py 8001     # 指定端口
"""
import asyncio
import sys
import socket
from app.main import app
import uvicorn


def check_port(host: str, port: int) -> bool:
    """检查端口是否被占用"""
    sock = None
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        return result == 0
    finally:
        if sock:
            sock.close()


def get_free_port(host: str, start_port: int) -> int:
    """获取可用端口"""
    port = start_port
    while check_port(host, port):
        print(f"端口 {port} 已被占用，尝试 {port + 1}...")
        port += 1
    return port


async def run_server():
    # 解析命令行参数
    host = '127.0.0.1'
    port = 8000

    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"错误: 端口号必须是整数，使用默认端口 8000")
            port = 8000

    # 检查并获取可用端口
    if check_port(host, port):
        print(f"端口 {port} 已被占用！")
        port = get_free_port(host, port)

    # 打印欢迎信息
    print("\n" + "=" * 60)
    print("  TaskTracker - 任务管理系统 API")
    print("=" * 60)
    print(f"\n  正在启动服务器...")
    print(f"  地址: http://{host}:{port}")
    print(f"  文档: http://{host}:{port}/docs")
    print(f"  ReDoc: http://{host}:{port}/redoc")
    print("\n  按 Ctrl+C 停止服务器\n")
    print("=" * 60 + "\n")

    # 启动服务器
    config = uvicorn.Config(
        app,
        host=host,
        port=port,
        log_level='info',
        reload=False
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == '__main__':
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        print('\n\n服务器已停止\n')
    except Exception as e:
        print(f'\n错误: {type(e).__name__}: {e}\n')
        sys.exit(1)

