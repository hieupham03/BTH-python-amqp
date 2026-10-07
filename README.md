# BÁO CÁO THỰC HÀNH: LẬP TRÌNH PYTHON VỚI GIAO THỨC AMQP (RABBITMQ)

## 1. Môi trường và Cấu hình Broker
- **Ngôn ngữ**: Python 3.x
- **Giao thức**: AMQP (Advanced Message Queuing Protocol 0-9-1)
- **Thư viện Python**: `pika`
- **Broker**: RabbitMQ
- **Cài đặt thư viện**:
  ```bash
  pip install pika
  ```

### Các cách triển khai RabbitMQ Broker:
1. **Chạy qua Docker (khuyến nghị, nhanh nhất)**:
   ```bash
   docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
   ```
   - Truy cập giao diện quản trị Web: `http://localhost:15672` (tài khoản: `guest` / `guest`).
2. **Cài đặt trực tiếp trên Windows**:
   - Tải Erlang và RabbitMQ Server từ trang chủ [rabbitmq.com](https://www.rabbitmq.com/).
3. **Sử dụng CloudAMQP (Miễn phí trên đám mây)**:
   - Đăng ký tài khoản tại [cloudamqp.com](https://www.cloudamqp.com/) (gói Little Lemur miễn phí).
   - Thiết lập biến môi trường `RABBITMQ_URL`:
     ```bash
     set RABBITMQ_URL=amqps://user:password@host/vhost
     ```

---

## 2. Cấu trúc các bài thực hành

### Thư mục `bai1/`: Gửi và nhận message cơ bản qua queue
- `producer_bai1.py`: Kết nối tới RabbitMQ, khai báo queue `iot_lab_queue` và gửi thông điệp chào mừng kèm thông tin sinh viên.
- `consumer_bai1.py`: Kết nối broker, lắng nghe hàng đợi `iot_lab_queue`, nhận và in thông điệp kèm thời gian nhận.
- `README.md`: Báo cáo chi tiết và hướng dẫn chạy Bài 1.

### Thư mục `bai2/`: Mô phỏng cảm biến IoT gửi dữ liệu môi trường
- `sensor_producer_bai2.py`: Mô phỏng cảm biến gửi dữ liệu nhiệt độ và độ ẩm định kỳ mỗi 3 giây dạng JSON vào queue `sensor_data_queue`.
- `monitor_consumer_bai2.py`: Lắng nghe dữ liệu, phân tích JSON và đưa ra cảnh báo khi nhiệt độ > 35°C hoặc độ ẩm < 40%.
- `README.md`: Báo cáo chi tiết và hướng dẫn chạy Bài 2.

### Thư mục `bai3/`: Mô phỏng hệ thống điều phối cảnh báo IoT với Exchange
- `alert_producer_bai3.py`: Khai báo direct exchange `iot_alert_exchange`, gửi thông điệp kèm routing key (`info`, `warning`, `critical`).
- `warning_consumer_bai3.py`: Tạo `warning_queue`, bind với routing key `warning` để chỉ nhận cảnh báo mức Warning.
- `critical_consumer_bai3.py`: Tạo `critical_queue`, bind với routing key `critical` để chỉ nhận cảnh báo mức Critical.
- `README.md`: Báo cáo chi tiết và hướng dẫn chạy Bài 3.
