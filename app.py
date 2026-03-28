from flask import Flask, render_template, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_FILE = 'aiotdb.db'

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    conn = get_db_connection()
    # 取得最近的 50 筆數據
    data = conn.execute('SELECT * FROM dht11_readings ORDER BY timestamp DESC LIMIT 50').fetchall()
    conn.close()
    
    # 轉換成 JSON 格式
    results = []
    for row in reversed(data): # 反轉讓時間軸是由舊到新
        results.append({
            'timestamp': row['timestamp'],
            'humidity': row['humidity'],
            'temperature': row['temperature']
        })
    return jsonify(results)

@app.route('/api/latest')
def get_latest():
    conn = get_db_connection()
    row = conn.execute('SELECT * FROM dht11_readings ORDER BY timestamp DESC LIMIT 1').fetchone()
    conn.close()
    
    if row:
        return jsonify({
            'timestamp': row['timestamp'],
            'humidity': row['humidity'],
            'temperature': row['temperature']
        })
    return jsonify({'error': 'No data found'}), 404

# --- 新增接收數據的接口 ---
from flask import request
@app.route('/api/upload', methods=['POST'])
def upload_data():
    data = request.get_json()
    if not data or 'humidity' not in data or 'temperature' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    
    humidity = data['humidity']
    temperature = data['temperature']
    
    try:
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO dht11_readings (humidity, temperature) VALUES (?, ?)",
            (humidity, temperature)
        )
        conn.commit()
        conn.close()
        print(f"收到無線傳輸：濕度 {humidity}%, 溫度 {temperature}°C")
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        print(f"資料庫寫入失敗: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # 確保資料庫檔案存在
    if not os.path.exists(DB_FILE):
        print(f"警告: 找不到 {DB_FILE}，請確認 logger.py 是否正在運行。")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
