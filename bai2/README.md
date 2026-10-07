# BÀI 2: MÔ PHỎNG CẢM BIẾN IOT GỬI DỮ LIỆU MÔI TRƯỜNG QUA AMQP

## 1. Broker sử dụng
- Broker: **RabbitMQ**
- Giao thức: **AMQP 0-9-1**
- Host mặc định: `localhost`
- Cổng mặc định: `5672`
- Queue sử dụng: `sensor_data_queue`
- Định dạng dữ liệu: **JSON** gồm `device_id`, `temperature`, `humidity`, `timestamp`.

## 2. Cách chạy từng chương trình

Mở 2 cửa sổ Terminal tại thư mục `bai2/`:

### Terminal 1 - Chạy Monitoring Consumer (Ứng dụng giám sát & cảnh báo):
```bash
python monitor_consumer_bai2.py
```
Chương trình kết nối đến queue `sensor_data_queue`, phân tích dữ liệu telemetry nhận được và tự động kích hoạt cảnh báo nếu vượt ngưỡng. Nhấn `Ctrl+C` để dừng.

### Terminal 2 - Chạy Sensor Producer (Mô phỏng cảm biến IoT):
```bash
python sensor_producer_bai2.py
```
Cứ mỗi 3 giây, chương trình sẽ tự động sinh dữ liệu nhiệt độ và độ ẩm ngẫu nhiên, đóng gói vào cấu trúc JSON và đẩy lên RabbitMQ queue `sensor_data_queue`.

> **Quy tắc cảnh báo:**
> - Nếu `nhiệt độ > 35°C`: Hiển thị `CANH BAO: Nhiet do cao`
> - Nếu `độ ẩm < 40%`: Hiển thị `CANH BAO: Do am thap`

## 3. Kết quả đạt được

### Output tại Terminal Sensor Producer:
```text
[*] Dang ket noi toi RabbitMQ broker (localhost:5672)...
[*] Bat dau mo phong cam bien gui du lieu vao queue 'sensor_data_queue' moi 3 giay.
[*] Nhan Ctrl+C de dung chuong trinh...

[Gui telemetry] {"device_id": "sensor01", "temperature": 36.4, "humidity": 38.9, "timestamp": "2026-10-07 14:10:03"}
[Gui telemetry] {"device_id": "sensor02", "temperature": 29.5, "humidity": 62.1, "timestamp": "2026-10-07 14:10:06"}
[Gui telemetry] {"device_id": "sensor03", "temperature": 38.2, "humidity": 45.0, "timestamp": "2026-10-07 14:10:09"}
```

### Output tại Terminal Monitoring Consumer:
```text
[*] Dang ket noi toi RabbitMQ broker (localhost:5672)...
[*] Dang theo doi du lieu tu queue 'sensor_data_queue'. Nhan Ctrl+C de dung...

Device: sensor01
Temperature: 36.4
Humidity: 38.9
Timestamp: 2026-10-07 14:10:03
CANH BAO: Nhiet do cao
CANH BAO: Do am thap
----------------------------------------
Device: sensor02
Temperature: 29.5
Humidity: 62.1
Timestamp: 2026-10-07 14:10:06
----------------------------------------
Device: sensor03
Temperature: 38.2
Humidity: 45.0
Timestamp: 2026-10-07 14:10:09
CANH BAO: Nhiet do cao
----------------------------------------
```

### Đánh giá:
- Payload dữ liệu tuân thủ chuẩn JSON dễ tích hợp và mở rộng.
- Dữ liệu cảm biến được truyền tuần hoàn 3s/lần qua AMQP queue ổn định, không mất mát gói tin.
- Consumer bắt sự kiện và phân tích đúng các ngưỡng cảnh báo quan trọng trong giám sát môi trường IoT.
