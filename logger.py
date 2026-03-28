import serial
import sqlite3
import re
import time
from datetime import datetime

# 設定序列埠參數
SERIAL_PORT = 'COM3'
BAUD_RATE = 115200
DB_FILE = 'sensor_data.db'

def init_db():
    """初始化 SQLite 資料庫與資料表"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dht11_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            humidity REAL,
            temperature REAL
        )
    ''')
    conn.commit()
    return conn

def main():
    print(f"與 {SERIAL_PORT} 連線中...")
    try:
        # 開啟序列埠
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # 等待序列埠穩定
        print("連線成功！開始監聽數據並寫入資料庫...")
        
        conn = init_db()
        cursor = conn.cursor()

        # 正規表達式用於解析數據：Humidity: 51.00%  Temperature: 31.20°C
        pattern = re.compile(r"Humidity:\s*([\d.]+)\s*%\s*Temperature:\s*([\d.]+)\s*°C")

        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if not line:
                    continue
                
                print(f"收到數據: {line}")
                
                # 嘗試匹配數據
                match = pattern.search(line)
                if match:
                    humidity = float(match.group(1))
                    temperature = float(match.group(2))
                    
                    # 寫入資料庫
                    try:
                        cursor.execute(
                            "INSERT INTO dht11_readings (humidity, temperature) VALUES (?, ?)",
                            (humidity, temperature)
                        )
                        conn.commit()
                        print(f"成功儲存：濕度 {humidity}%, 溫度 {temperature}°C")
                    except sqlite3.Error as e:
                        print(f"資料庫寫入錯誤: {e}")
                
    except serial.SerialException as e:
        print(f"序列埠錯誤: {e}")
    except KeyboardInterrupt:
        print("\n使用者停止執行。")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
        if 'conn' in locals():
            conn.close()
        print("資源已釋放。")

if __name__ == "__main__":
    main()
