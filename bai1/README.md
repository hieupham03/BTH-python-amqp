# BÀI 1: GỬI VÀ NHẬN MESSAGE CƠ BẢN QUA QUEUE TRONG AMQP

## 1. Broker sử dụng
- Broker: **RabbitMQ**
- Giao thức: **AMQP 0-9-1**
- Host mặc định: `localhost` (hoặc IP broker của lớp / CloudAMQP)
- Cổng mặc định: `5672` (AMQP tiêu chuẩn)
- Queue sử dụng: `iot_lab_queue`
- Thư viện Python: `pika`

## 2. Cách chạy từng chương trình

Cài đặt thư viện AMQP nếu chưa có:
```bash
pip install pika
```

Mở 2 cửa sổ Terminal tại thư mục `bai1/`:

### Terminal 1 - Chạy Consumer (Lắng nghe queue):
```bash
python consumer_bai1.py
```
Chương trình kết nối đến RabbitMQ broker và lắng nghe tin nhắn từ hàng đợi `iot_lab_queue`. Nhấn `Ctrl+C` để dừng.

### Terminal 2 - Chạy Producer (Gửi message):
```bash
python producer_bai1.py
```
Hoặc gửi message tùy chỉnh:
```bash
python producer_bai1.py "Xin chao tu ung dung Python AMQP - B23DCCN001 - Nguyen Van A"
```

> **Lưu ý cấu hình Broker:**
> Nếu sử dụng broker từ xa hoặc CloudAMQP, bạn có thể truyền biến môi trường trước khi chạy:
> ```bash
> set RABBITMQ_HOST=192.168.1.50
> set RABBITMQ_PORT=5672
> set RABBITMQ_USER=guest
> set RABBITMQ_PASS=guest
> # Hoặc dùng chuỗi URL:
> set RABBITMQ_URL=amqp://guest:guest@localhost:5672/%2f
> ```

## 3. Kết quả đạt được

### Output tại Terminal Producer:
```text
[*] Dang ket noi toi RabbitMQ broker (localhost:5672)...
[x] Da gui message: 'Xin chao tu ung dung Python AMQP - B23DCCN001 - Nguyen Van A' vao queue 'iot_lab_queue'
[*] Hoan tat va da ngat ket noi.
```

### Output tại Terminal Consumer:
```text
[*] Dang ket noi toi RabbitMQ broker (localhost:5672)...
[*] Dang cho message tu queue 'iot_lab_queue'. Nhan Ctrl+C de thoat...
Da nhan message: Xin chao tu ung dung Python AMQP - B23DCCN001 - Nguyen Van A
Thoi gian nhan: 14:05:21
----------------------------------------
```

### Đánh giá:
- Kết nối thành công đến RabbitMQ broker qua giao thức AMQP.
- Producer gửi dữ liệu vào queue `iot_lab_queue` ổn định và tin nhắn được lưu trữ bền vững (durable).
- Consumer nhận dữ liệu theo cơ chế đẩy (push), hiển thị chính xác nội dung thông điệp kèm mốc thời gian nhận thực tế.
