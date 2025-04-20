from fastapi import FastAPI, HTTPException
import sqlite3
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Database setup
def init_db():
    conn = sqlite3.connect('functions.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS functions
                 (id INTEGER PRIMARY KEY, name TEXT, route TEXT, language TEXT, timeout INTEGER, code TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS metrics
                 (id INTEGER PRIMARY KEY, func_id INTEGER, execution_time REAL, success BOOLEAN, cpu_usage INTEGER, memory_usage INTEGER, timestamp TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Pydantic models
class Function(BaseModel):
    name: str
    route: str
    language: str
    timeout: int
    code: Optional[str] = None

class Metric(BaseModel):
    func_id: int
    execution_time: float
    success: bool
    cpu_usage: int
    memory_usage: int
    timestamp: str

# CRUD Endpoints for Functions
@app.post('/functions/')
def create_function(func: Function):
    conn = sqlite3.connect('functions.db')
    c = conn.cursor()
    c.execute('INSERT INTO functions (name, route, language, timeout, code) VALUES (?, ?, ?, ?, ?)',
              (func.name, func.route, func.language, func.timeout, func.code))
    conn.commit()
    conn.close()
    return {'message': 'Function created', 'function': func}

@app.get('/functions/{func_id}')
def get_function(func_id: int):
    conn = sqlite3.connect('functions.db')
    c = conn.cursor()
    c.execute('SELECT * FROM functions WHERE id = ?', (func_id,))
    func = c.fetchone()
    conn.close()
    if func:
        return {'id': func[0], 'name': func[1], 'route': func[2], 'language': func[3], 'timeout': func[4], 'code': func[5]}
    raise HTTPException(status_code=404, detail='Function not found')

@app.put('/functions/{func_id}')
def update_function(func_id: int, func: Function):
    conn = sqlite3.connect('functions.db')
    c = conn.cursor()
    c.execute('UPDATE functions SET name = ?, route = ?, language = ?, timeout = ?, code = ? WHERE id = ?',
              (func.name, func.route, func.language, func.timeout, func.code, func_id))
    conn.commit()
    conn.close()
    return {'message': 'Function updated'}

@app.delete('/functions/{func_id}')
def delete_function(func_id: int):
    conn = sqlite3.connect('functions.db')
    c = conn.cursor()
    c.execute('DELETE FROM functions WHERE id = ?', (func_id,))
    conn.commit()
    conn.close()
    return {'message': 'Function deleted'}

# Metrics Endpoint
@app.post('/metrics/')
def log_metric(metric: Metric):
    conn = sqlite3.connect('functions.db')
    c = conn.cursor()
    c.execute('INSERT INTO metrics (func_id, execution_time, success, cpu_usage, memory_usage, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
              (metric.func_id, metric.execution_time, metric.success, metric.cpu_usage, metric.memory_usage, metric.timestamp))
    conn.commit()
    conn.close()
    return {'message': 'Metric logged'}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)