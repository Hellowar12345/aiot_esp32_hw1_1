import sqlite3

def view_data():
    try:
        conn = sqlite3.connect('aiotdb.db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM dht11_readings ORDER BY timestamp DESC LIMIT 10')
        rows = cur.fetchall()
        
        print(f"| {'ID':<5} | {'Timestamp':<20} | {'Humidity (%)':<12} | {'Temperature (°C)':<16} |")
        print("-" * 65)
        for r in rows:
            print(f"| {r[0]:<5} | {r[1]:<20} | {r[2]:<12.2f} | {r[3]:<16.2f} |")
            
        conn.close()
    except Exception as e:
        print(e)
        
if __name__ == '__main__':
    view_data()
