# ESP32 IoT 專案開發歷程報告 (2026-03-11)

---

## 🟢 第一階段：LED Flash (燈閃爍測試)

*   **您的需求 (User Request)**：
    「寫個 arduino 程式並運行讓我的 esp32 的 led 能夠亮起來。」
*   **我的執行 (Action)**：
    -   撰寫 Arduino 程式碼，定義使用 ESP32 內建 LED (GPIO 2)。
    -   設定每隔 1 秒切換一次高低電位 (HIGH/LOW)。
    -   協助安裝 USB 驅動程式 (CP2102) 以建立 COM Port 連線。
*   **成果展示 (Result)**：
    -   程式編譯完成並成功上傳。
    -   ESP32 板載藍色 LED 開始規律閃爍。


*   **程式碼實作 (Programming)**：
```cpp
#define LED_PIN 2

void setup() {
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  digitalWrite(LED_PIN, HIGH);
  delay(1000);
  digitalWrite(LED_PIN, LOW);
  delay(1000);
}
```

> <img src="IMG_0177.PNG" width="500">

---

## 🔵 第二階段：DHT11 Data shown on Serial port (感測數據讀取)

*   **您的需求 (User Request)**：
    「接 DHT11 到 esp32，然後把收集到的數據 print 出來。」
*   **我的執行 (Action)**：
    -   引入 `DHT sensor library` 函式庫。
    -   撰寫讀取程式碼，並在 `Serial.print` 輸出格式化的溫溼度字串。
    -   **硬體調試**：將數據腳位由 D15 改至 **D4 (GPIO 4)** 以獲得更穩定的讀取。
*   **成果展示 (Result)**：
    -   **Serial Monitor 顯示結果**：
        ```text
        --- ESP32 DHT11 測試啟動 ---
        Humidity: 33.00%  Temperature: 25.20°C
        Humidity: 44.00%  Temperature: 25.60°C
        Humidity: 42.00%  Temperature: 26.00°C
        ```

*   **程式碼實作 (Programming)**：
```cpp
#include "DHT.h"
#define DHTPIN 4
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  dht.begin();
}

void loop() {
  delay(2000);
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  Serial.print("Humidity: ");
  Serial.print(h);
  Serial.print("%  Temperature: ");
  Serial.print(t);
  Serial.println("°C");
}
```

---

## 🟡 第三階段：aiotdb.db Data in SQLite3 (資料庫儲存)

*   **您的需求 (User Request)**：
    「我想將感測到的數據透過 python 寫到 sqlite。」
*   **我的執行 (Action)**：
    -   設定資料庫名稱為 `aiotdb.db`。
    -   撰寫 Python 橋接腳本，開啟序列埠監聽，並將解析後的 JSON/文字數據存入 SQL Table。
    -   建立 `dht11_readings` 資料表，包含 `id`, `timestamp`, `humidity`, `temperature` 四個欄位。
*   **成果展示 (Result)**：
    -   在 SQLite3 Viewer 中可以看到感測器的即時紀錄。
    -   **資料庫內容預覽**：
        | id | timestamp | humidity | temperature |
        |---|---|---|---|
        | 1 | 2026-03-11 17:00:01 | 33.0 | 25.2 |
        | 2 | 2026-03-11 17:00:06 | 44.0 | 25.6 |

---

## 🔴 第四階段：Via WiFi 成功 (無線 IoT 傳輸)

*   **您的需求 (User Request)**：
    「我想透過手機當 ap 來上傳 dht11 的資料到電腦 server。」
*   **我的執行 (Action)**：
    -   **手機設定**：引導開啟 iPhone 熱點「最大化相容性 (2.4GHz)」。
    -   **程式升級**：將 ESP32 程式改為 WiFi Client 模式，連線至 SSID `iPhone (138)`。
    -   **前後端整合**：架設 Flask Server 接收 `HTTP POST` 請求，並結合 Chart.js 繪製動態網頁圖表。
*   **成果展示 (Result)**：
    -   **連線成功 Log**：
        ```text
        正在連線至 Wi-Fi: iPhone (138)...
        Wi-Fi 已連線！ ESP32 IP 位址: 172.20.10.2
        🌐 正在透過 WiFi 傳送數據...
        ✅ 傳送成功！回應碼: 200
        ```
    -   **網頁展示**：透過 `http://127.0.0.1:5000` 即可看到無線傳輸的數據波形。

---

## ⚙️ 技術總結與問題解決 (Technical Summary)

| 遇到的挑戰 | 原因分析 | 解決方案 |
| :--- | :--- | :--- |
| **找不到 COM Port** | 缺少 USB 轉串口驅動 | 手動下載並安裝 CP2102 VCP 驅動程式 |
| **上傳失敗 (Boot mode)** | ESP32 未進入燒錄狀態 | 上傳時持續按住板上的 **BOOT** 按鈕 |
| **WiFi 連不上** | SSID 中有空格及多頻段影響 | 修正 SSID 為 `"iPhone (138)"` 並在手機開啟「最大化相容性」 |
| **數據讀取失敗 (NaN)** | 腳位訊號干擾或接線不良 | 將訊號線從 **D15** 遷移至 **D4** |
| **伺服器連不上** | 電腦防火牆阻擋 Port 5000 | 關閉防火牆或手動放行 TCP 5000 埠口 |

---
**本報告由 Antigravity AI 助手整理開發流程。**
