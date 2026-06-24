import socket
import sys
from datetime import datetime

# Направляем сканер на официальный сайт Kali Linux
target_host = "kali.org"

print("-" * 50)
print(f"Сканирование хоста: {target_host}")
print(f"Время запуска: {str(datetime.now())}")
print("-" * 50)

# Порты 80 (HTTP) и 443 (HTTPS) на сайтах в интернете обязаны быть открыты
ports_to_scan = [21, 22, 80, 443, 8080]

try:
    for port in ports_to_scan:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0) # Дадим чуть больше времени на ответ через интернет
        result = s.connect_ex((target_host, port))
        
        if result == 0:
            print(f"Порт {port}: ОТКРЫТ [Предупреждение]")
        else:
            print(f"Порт {port}: Закрыт")
        s.close()

except KeyboardInterrupt:
    print("\nСканирование прервано.")
    sys.exit()

except socket.error:
    print("\nОшибка сети.")
    sys.exit()
