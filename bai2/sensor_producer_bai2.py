import os
import sys
import time
import json
import random
from datetime import datetime
import pika

# Cấu hình Broker RabbitMQ (có thể ghi đè bằng biến môi trường)
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")
RABBITMQ_URL = os.getenv("RABBITMQ_URL", None)

QUEUE_NAME = "sensor_data_queue"
DEVICES = ["sensor01", "sensor02", "sensor03"]

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

def main():
    try:
        print(f"[*] Dang ket noi toi RabbitMQ broker ({RABBITMQ_HOST}:{RABBITMQ_PORT})...")
        connection = get_connection()
        channel = connection.channel()

        # Khai báo queue sensor_data_queue
        channel.queue_declare(queue=QUEUE_NAME, durable=True)
        print(f"[*] Bat dau mo phong cam bien gui du lieu vao queue '{QUEUE_NAME}' moi 3 giay.")
        print("[*] Nhan Ctrl+C de dung chuong trinh...\n")

        device_index = 0
        while True:
            # Luân phiên hoặc tập trung vào sensor01
            device_id = DEVICES[device_index % len(DEVICES)]
            device_index += 1

            # Sinh nhiệt độ ngẫu nhiên từ 22.0 đến 42.0 độ C
            # Sinh độ ẩm ngẫu nhiên từ 30.0% đến 85.0%
            temperature = round(random.uniform(22.0, 42.0), 1)
            humidity = round(random.uniform(30.0, 85.0), 1)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            payload = {
                "device_id": device_id,
                "temperature": temperature,
                "humidity": humidity,
                "timestamp": timestamp
            }

            payload_json = json.dumps(payload, ensure_ascii=False)

            channel.basic_publish(
                exchange="",
                routing_key=QUEUE_NAME,
                body=payload_json.encode("utf-8"),
                properties=pika.BasicProperties(
                    delivery_mode=pika.DeliveryMode.Persistent,
                    content_type="application/json"
                )
            )

            print(f"[Gui telemetry] {payload_json}")
            time.sleep(3)

    except KeyboardInterrupt:
        print("\n[*] Nguoi dung dung chuong trinh. Dang ngat ket noi...")
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
