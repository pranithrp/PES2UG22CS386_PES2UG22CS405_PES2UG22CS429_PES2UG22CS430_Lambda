import docker
import time
import os
import sqlite3
import datetime
from packager import package_function
from load_balancer import LoadBalancer

client = docker.from_env()
load_balancer = LoadBalancer(['node1', 'node2'])  # Simulate two nodes

def log_metric(func_id, execution_time, success, cpu_usage, memory_usage):
    conn = sqlite3.connect('backend/functions.db')
    c = conn.cursor()
    timestamp = datetime.datetime.now().isoformat()
    c.execute('INSERT INTO metrics (func_id, execution_time, success, cpu_usage, memory_usage, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (func_id, execution_time, success, cpu_usage, memory_usage, timestamp))
    conn.commit()
    conn.close()

def execute_function(func_id, language, code, timeout):
    func_dir = package_function(func_id, language, code)
    image = 'lambda-python' if language == 'python' else 'lambda-javascript'
    node = load_balancer.get_next_node()
    try:
        start_time = time.time()
        container = client.containers.run(
            image,
            volumes={f'{os.getcwd()}/{func_dir}': {'bind': '/app', 'mode': 'rw'}},
            detach=True,
            mem_limit='128m',
            cpu_quota=50000
        )
        while time.time() - start_time < timeout:
            container.reload()
            if container.status == 'exited':
                logs = container.logs().decode()
                container.remove()
                execution_time = time.time() - start_time
                log_metric(func_id, execution_time, True, 50, 128)  # Simulated CPU/memory
                return logs
            time.sleep(0.1)
        container.kill()
        container.remove()
        execution_time = time.time() - start_time
        log_metric(func_id, execution_time, False, 50, 128)
        return 'Function timed out'
    except Exception as e:
        execution_time = time.time() - start_time
        log_metric(func_id, execution_time, False, 50, 128)
        return f'Error: {str(e)}'

if __name__ == '__main__':
    result = execute_function(1, 'python', 'print(\"Hello, Lambda!\")', 30)
    print(result)