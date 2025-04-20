import docker
import time
import os
from packager import package_function

client = docker.from_env()

def execute_function(func_id, language, code, timeout):
    func_dir = package_function(func_id, language, code)
    image = 'lambda-python' if language == 'python' else 'lambda-javascript'
    volume_path = os.path.abspath(func_dir)

    try:
        container = client.containers.run(
            image=image,
            volumes={volume_path: {'bind': '/app', 'mode': 'rw'}},
            working_dir='/app',
            detach=True,
            mem_limit='128m',
            cpu_quota=50000
        )

        start_time = time.time()
        while time.time() - start_time < timeout:
            container.reload()
            if container.status == 'exited':
                logs = container.logs().decode()
                container.remove()
                return logs
            time.sleep(0.1)

        container.kill()
        container.remove()
        return 'Function timed out'
    except Exception as e:
        return f'Error: {str(e)}'

# For manual testing
if __name__ == '__main__':
    result = execute_function(
        func_id=1,
        language='python',
        code='print("Hello, Lambda!")',
        timeout=5
    )
    print(result)
