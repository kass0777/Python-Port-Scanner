import socket
import sys
import time
from datetime import datetime

# Сканируем локальный хост (самого себя) для безопасности
target_host = "127.0.0.1" 

print("-" * 50)
print(f"Запуск глубокого сканирования хоста: {target_host}")
print(f"Время: {str(datetime.now())}")
print("-" * 50)

# Список портов для проверки
ports_to_scan = [21, 22, 80, 443, 8080]

try:
    for port in ports_to_scan:
        # Соблюдаем лимит Bug Bounty (пауза 0.4 сек, чтобы было меньше 4 запросов в секунду)
        time.sleep(0.4)
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.5)
        
        result = s.connect_ex((target_host, port))
        
        if result == 0:
            print(f"[+] Порт {port}: ОТКРЫТ")
            
            # Пытаемся выудить баннер (скрытую информацию сервиса)
            try:
                s.send(b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n")
                banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
                if banner:
                    # Берем только первую строчку ответа для красоты в консоли
                    first_line = banner.split('\n')[0]
                    print(f"    └── [Глубокий анализ] Сервер ответил: {first_line}")
            except Exception:
                print(f"    └── [Глубокий анализ] Не удалось считать баннер")
        else:
            print(f"[-] Порт {port}: закрыт")
            
        s.close()

except KeyboardInterrupt:
    print("\nСканирование прервано пользователем.")
    sys.exit()
except socket.error:
    print("\nОшибка сети.")
    sys.exit()
