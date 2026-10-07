# BÀI 3: MÔ PHỎNG HỆ THỐNG ĐIỀU PHỐI CẢNH BÁO IOT VỚI DIRECT EXCHANGE

## 1. Broker sử dụng
- Broker: **RabbitMQ**
- Giao thức: **AMQP 0-9-1**
- Host mặc định: `localhost`
- Cổng mặc định: `5672`
- Exchange sử dụng: `iot_alert_exchange` (loại **direct**)
- Queues & Routing Keys:
  - `warning_queue` được bind với exchange bằng routing key `warning`
  - `critical_queue` được bind với exchange bằng routing key `critical`
  - Mức `info`: không có queue nào bind, message không được gửi tới 2 queue trên

## 2. Cách chạy từng chương trình

Mở 3 cửa sổ Terminal tại thư mục `bai3/`:

### Terminal 1 - Chạy Warning Consumer:
```bash
python warning_consumer_bai3.py
```
Chương trình tạo queue `warning_queue` và bind vào `iot_alert_exchange` với routing key `warning`. Chỉ lắng nghe và hiển thị cảnh báo mức Warning.

### Terminal 2 - Chạy Critical Consumer:
```bash
python critical_consumer_bai3.py
```
Chương trình tạo queue `critical_queue` và bind vào `iot_alert_exchange` với routing key `critical`. Chỉ lắng nghe và hiển thị cảnh báo mức Critical.

### Terminal 3 - Chạy Alert Producer:
```bash
python alert_producer_bai3.py
```
Giao diện dòng lệnh cung cấp menu để gửi tin nhắn theo ý muốn:
- Nhấn phím `1`: Gửi cảnh báo mức `info`
- Nhấn phím `2`: Gửi cảnh báo mức `warning`
- Nhấn phím `3`: Gửi cảnh báo mức `critical`
- Nhấn phím `4`: Chạy kịch bản tự động gửi cả 3 mức liên tiếp

*(Hoặc chạy nhanh chế độ demo tự động: `python alert_producer_bai3.py --demo`)*

## 3. Kết quả đạt được

### Khi Alert Producer gửi 3 thông điệp mẫu:
1. `info`: "Thiet bi cam bien da ket noi va hoat dong binh thuong info"
2. `warning`: "Nhiet do phong may vuot nguong warning"
3. `critical`: "Cam bien kho lanh mat ket noi critical"

### Terminal Alert Producer:
```text
[*] Direct exchange 'iot_alert_exchange' da san sang.
[*] Dang gui chuoi 3 message mau theo de bai:
[x] Da gui -> Exchange: 'iot_alert_exchange' | Routing Key: 'info' | Message: 'Thiet bi cam bien da ket noi va hoat dong binh thuong info'
[x] Da gui -> Exchange: 'iot_alert_exchange' | Routing Key: 'warning' | Message: 'Nhiet do phong may vuot nguong warning'
[x] Da gui -> Exchange: 'iot_alert_exchange' | Routing Key: 'critical' | Message: 'Cam bien kho lanh mat ket noi critical'
[*] Hoan tat gui chuoi 3 message demo.
```

### Terminal Warning Consumer:
```text
[*] [warning_queue] Dang cho tin nhan routing key 'warning' tu 'iot_alert_exchange'...
[warning_queue] [14:15:02] Da nhan: Nhiet do phong may vuot nguong warning
```

### Terminal Critical Consumer:
```text
[*] [critical_queue] Dang cho tin nhan routing key 'critical' tu 'iot_alert_exchange'...
[critical_queue] [14:15:03] Da nhan: Cam bien kho lanh mat ket noi critical
```

### Nhận xét & Đánh giá:
- Message có routing key `info` không bị nhận bởi `warning_queue` và `critical_queue`, đúng theo cơ chế định tuyến của **Direct Exchange**.
- Message có routing key `warning` chỉ được chuyển giao tới `warning_queue`.
- Message có routing key `critical` chỉ được chuyển giao tới `critical_queue`.
- Cơ chế Direct Exchange giúp phân loại và phân luồng thông điệp cảnh báo trong hệ thống IoT một cách chính xác, bảo mật và hiệu năng cao.
