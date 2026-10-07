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

EXCHANGE_NAME = "iot_alert_exchange"
QUEUE_NAME = "warning_queue"
ROUTING_KEY = "warning"

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
    time_str = datetime.now().strftime("%H:%M:%S")
    message = body.decode("utf-8")
    print(f"[{QUEUE_NAME}] [{time_str}] Da nhan: {message}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    try:
        print(f"[*] Dang ket noi toi RabbitMQ broker ({RABBITMQ_HOST}:{RABBITMQ_PORT})...")
        connection = get_connection()
        channel = connection.channel()

        # Khai báo direct exchange
        channel.exchange_declare(
            exchange=EXCHANGE_NAME,
            exchange_type="direct",
            durable=True
        )

        # Khai báo queue warning_queue
        channel.queue_declare(queue=QUEUE_NAME, durable=True)

        # Ràng buộc (bind) queue với exchange bằng routing key 'warning'
        channel.queue_bind(
            exchange=EXCHANGE_NAME,
            queue=QUEUE_NAME,
            routing_key=ROUTING_KEY
        )

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)

        print(f"[*] [{QUEUE_NAME}] Dang cho tin nhan routing key '{ROUTING_KEY}' tu '{EXCHANGE_NAME}'...")
        print("[*] Nhan Ctrl+C de dung...\n")
        channel.start_consuming()

    except KeyboardInterrupt:
        print("\n[*] Nguoi dung dung chuong trinh. Dang thoat...")
        try:
            connection.close()
        except Exception:
            pass
        sys.exit(0)
    except Exception as e:
        print(f"[!] Loi: {e}")
        print("[*] Goi y: Kiem tra dich vu RabbitMQ da bat chua.")

if __name__ == "__main__":
    main()
