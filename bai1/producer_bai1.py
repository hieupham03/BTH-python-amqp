import os
import sys
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

def main():
    message = "Xin chao tu ung dung Python AMQP - B23DCCN001 - Nguyen Van A"
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])

    try:
        print(f"[*] Dang ket noi toi RabbitMQ broker ({RABBITMQ_HOST}:{RABBITMQ_PORT})...")
        connection = get_connection()
        channel = connection.channel()

        # Khai báo queue
        channel.queue_declare(queue=QUEUE_NAME, durable=True)

        # Gửi thông điệp vào queue
        channel.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
            body=message.encode("utf-8"),
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent
            )
        )
        print(f"[x] Da gui message: '{message}' vao queue '{QUEUE_NAME}'")

        connection.close()
        print("[*] Hoan tat va da ngat ket noi.")
    except Exception as e:
        print(f"[!] Loi ket noi hoac gui message: {e}")
        print("[*] Goi y: Hay kiem tra xem RabbitMQ da duoc khoi chay tren may chua,")
        print("    hoac thiet lap bien moi truong RABBITMQ_HOST / RABBITMQ_URL.")

if __name__ == "__main__":
    main()
