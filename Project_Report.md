# ESP32 IoT 專案開發總結報告
**日期：** 2026年3月11日
**專案名稱：** 無線溫溼度監控系統 (DHT11 + Flask + SQLite)

---

## 1. 執行目標與需求
本專案旨在建立一個完整的物聯網系統，包含從硬體感測到雲端可視化的所有流程。

### 輸入需求：
- **LED 控制**：讓 ESP32 內建 LED 閃爍。
- **感測整合**：連接 DHT11 並在序列埠顯示數據。
- **資料儲存**：將數據透過 Python 寫入 SQLite 資料庫。
- **網頁監控**：使用 Flask 架設網頁 dashboard 並顯示圖表。
- **無線傳輸**：透過手機熱點分享，實現無線上傳數據至 Server。

---

## 2. 硬體配置 (Hardware)
- **開發板**：ESP32 Dev Module
- **感測器**：DHT11 溫溼度感測器
- **接線定義**：
    - VCC -> ESP32 3.3V
    - GND -> ESP32 GND
    - **Signal (S) -> GPIO 4 (D4)** (最終穩定腳位)
- **Wi-Fi 連線**：
    - SSID: `iPhone (138)`
    - Password: `77777777`

---

## 3. 軟體架構 (Software)

### 嵌入式端 (Arduino/C++)
- 使用 `WiFi.h` 及 `HTTPClient.h` 連接 API。
- 使用 `ArduinoJson` 處理數據封裝。
- 定時每 5 秒讀取一次數據並發送 HTTP POST 請求。

### 伺服器端 (Python/Flask)
- **後端程式** (`app.py`)：接收 POST 請求並寫入 `sensor_data.db`。
- **資料庫**：SQLite，表名 `dht11_readings`。
- **前端網頁** (`index.html`)：
    - 採用現代化 **Glassmorphism** 設計風格。
    - 使用 **Chart.js** 繪製動態溫溼度曲線圖。
    - 自動刷新機制，無需手動整理。

---

## 4. 解決的問題紀錄 (Troubleshooting)
1. **驅動程式**：安裝 Silicon Labs CP210x 驅動程式解決 COM Port 無法識別。
2. **燒錄模式**：引導使用 BOOT 按鈕解決 `Wrong boot mode` 報錯。
3. **Wi-Fi 連線**：修正 SSID 名稱空格問題，並開啟 iPhone 「最大化相容性」以支援 2.4GHz。
4. **數據失敗**：將 DHT11 從 D15 移至 D4，解決了感測器讀取失敗的問題。
5. **電腦 IP**：確認熱點下的電腦 IP 為 `172.20.10.3` 並正確對應至 ESP32 程式碼。

---

## 5. 檔案位置參考 (File Locations)
- **Arduino 專案**：`C:\Users\linmaggie\.gemini\antigravity\scratch\esp32_led_pio`
- **Python 資料記錄器與伺服器**：`C:\Users\linmaggie\.gemini\antigravity\scratch\esp32_data_logger`
- **資料庫路徑**：`C:\Users\linmaggie\.gemini\antigravity\scratch\esp32_data_logger\sensor_data.db`

---
**報告結束**
報告由 Antigravity AI 整理。
