import os

def package_function(func_id, language, code):
    func_dir = f'functions/{func_id}'
    os.makedirs(func_dir, exist_ok=True)

    if language == 'python':
        file_path = os.path.join(func_dir, 'function.py')
    elif language == 'javascript':
        file_path = os.path.join(func_dir, 'function.js')
    else:
        raise ValueError('Unsupported language')

    with open(file_path, 'w') as f:
        f.write(code)

    return func_dir
