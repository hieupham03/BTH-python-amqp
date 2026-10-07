import os
import sys
import time
import pika

# Cấu hình Broker RabbitMQ (có thể ghi đè bằng biến môi trường)
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")
RABBITMQ_URL = os.getenv("RABBITMQ_URL", None)

EXCHANGE_NAME = "iot_alert_exchange"

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

def send_alert(channel, routing_key, message):
    channel.basic_publish(
        exchange=EXCHANGE_NAME,
        routing_key=routing_key,
        body=message.encode("utf-8"),
        properties=pika.BasicProperties(
            delivery_mode=pika.DeliveryMode.Persistent
        )
    )
    print(f"[x] Da gui -> Exchange: '{EXCHANGE_NAME}' | Routing Key: '{routing_key}' | Message: '{message}'")

def run_demo(channel):
    print("\n[*] Dang gui chuoi 3 message mau theo de bai:")
    time.sleep(0.5)

    msg_info = "Thiet bi cam bien da ket noi va hoat dong binh thuong info"
    send_alert(channel, "info", msg_info)
    time.sleep(1)

    msg_warning = "Nhiet do phong may vuot nguong warning"
    send_alert(channel, "warning", msg_warning)
    time.sleep(1)

    msg_critical = "Cam bien kho lanh mat ket noi critical"
    send_alert(channel, "critical", msg_critical)
    print("[*] Hoan tat gui chuoi 3 message demo.\n")

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
        print(f"[*] Direct exchange '{EXCHANGE_NAME}' da san sang.")

        if len(sys.argv) > 1 and sys.argv[1] == "--demo":
            run_demo(channel)
            connection.close()
            return

        while True:
            print("\n================= MENU ALERT PRODUCER =================")
            print("1. Gui canh bao cap do INFO     (Routing key: info)")
            print("2. Gui canh bao cap do WARNING  (Routing key: warning)")
            print("3. Gui canh bao cap do CRITICAL (Routing key: critical)")
            print("4. Chay kich ban demo (gui ca 3 message lan luot)")
            print("0. Thoat chuong trinh")
            print("========================================================")
            choice = input("Chon thao tac (0-4): ").strip()

            if choice == "1":
                msg = input("Nhap noi dung info (Enter de lay mac dinh): ").strip()
                if not msg:
                    msg = "Thiet bi cam bien da ket noi va hoat dong binh thuong info"
                send_alert(channel, "info", msg)
            elif choice == "2":
                msg = input("Nhap noi dung warning (Enter de lay mac dinh): ").strip()
                if not msg:
                    msg = "Nhiet do phong may vuot nguong warning"
                send_alert(channel, "warning", msg)
            elif choice == "3":
                msg = input("Nhap noi dung critical (Enter de lay mac dinh): ").strip()
                if not msg:
                    msg = "Cam bien kho lanh mat ket noi critical"
                send_alert(channel, "critical", msg)
            elif choice == "4":
                run_demo(channel)
            elif choice == "0":
                print("[*] Dang thoat chuong trinh...")
                break
            else:
                print("[!] Lua chon khong hop le, vui long chon lai.")

        connection.close()
    except KeyboardInterrupt:
        print("\n[*] Nguoi dung dung chuong trinh.")
        try:
            connection.close()
        except Exception:
            pass
    except Exception as e:
        print(f"[!] Loi: {e}")
        print("[*] Goi y: Kiem tra dich vu RabbitMQ da bat chua.")

if __name__ == "__main__":
    main()
