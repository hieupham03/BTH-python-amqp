import os
import sys
import json
import pika

# Cấu hình Broker RabbitMQ (có thể ghi đè bằng biến môi trường)
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")
RABBITMQ_URL = os.getenv("RABBITMQ_URL", None)

QUEUE_NAME = "sensor_data_queue"

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
    try:
        data = json.loads(body.decode("utf-8"))
        device_id = data.get("device_id", "Unknown")
        temperature = data.get("temperature", 0.0)
        humidity = data.get("humidity", 0.0)
        timestamp = data.get("timestamp", "")

        print(f"Device: {device_id}")
        print(f"Temperature: {temperature}")
        print(f"Humidity: {humidity}")
        if timestamp:
            print(f"Timestamp: {timestamp}")

        # Kiểm tra ngưỡng cảnh báo
        if temperature > 35:
            print("CANH BAO: Nhiet do cao")
        if humidity < 40:
            print("CANH BAO: Do am thap")

        print("-" * 40)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except json.JSONDecodeError:
        print(f"[!] Loi parse JSON tu payload: {body.decode('utf-8', errors='ignore')}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as err:
        print(f"[!] Loi xu ly telemetry: {err}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    try:
        print(f"[*] Dang ket noi toi RabbitMQ broker ({RABBITMQ_HOST}:{RABBITMQ_PORT})...")
        connection = get_connection()
        channel = connection.channel()

        channel.queue_declare(queue=QUEUE_NAME, durable=True)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)

        print(f"[*] Dang theo doi du lieu tu queue '{QUEUE_NAME}'. Nhan Ctrl+C de dung...\n")
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
