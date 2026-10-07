import os
import sys
from datetime import datetime
import pika

# Cấu hình Broker RabbitMQ (có thể ghi đè bằng biến môi trường)
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")
RABBITMQ_URL = os.getenv("RABBITMQ_URL", None)

QUEUE_NAME = "iot_lab_queue"

def get_connection():
    if RABBITMQ_URL:
        params = pika.URLParameters(RABBITMQ_URL)
        return pika.BlockingConnection(params)
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    params = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        credentials=credentials
    )
    return pika.BlockingConnection(params)

def callback(ch, method, properties, body):
    now_str = datetime.now().strftime("%H:%M:%S")
    message = body.decode("utf-8")
    print(f"Da nhan message: {message}")
    print(f"Thoi gian nhan: {now_str}")
    print("-" * 40)

    # Xác nhận đã xử lý message thành công
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    try:
        print(f"[*] Dang ket noi toi RabbitMQ broker ({RABBITMQ_HOST}:{RABBITMQ_PORT})...")
        connection = get_connection()
        channel = connection.channel()

        channel.queue_declare(queue=QUEUE_NAME, durable=True)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)

        print(f"[*] Dang cho message tu queue '{QUEUE_NAME}'. Nhan Ctrl+C de thoat...")
        channel.start_consuming()

    except KeyboardInterrupt:
        print("\n[*] Nguoi dung dung chuong trinh. Dang thoat...")
        try:
            connection.close()
        except Exception:
            pass
        sys.exit(0)
    except Exception as e:
        print(f"[!] Loi ket noi hoac lang nghe: {e}")
        print("[*] Goi y: Kiem tra dich vu RabbitMQ da duoc bat tai dia chi tren.")

if __name__ == "__main__":
    main()
