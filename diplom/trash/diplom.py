from prometheus_client import start_http_server, Gauge
import subprocess
import yaml
import time
import os
from tqdm import tqdm

# Определение показателей Prometheus
CPU_METRIC = Gauge('cpu_usage_percent', 'CPU usage percent')
MEMORY_METRIC = Gauge('memory_usage_percent', 'Memory usage percent')

# Определение пороговых значений ресурсов
CPU_THRESHOLD = 80.0
MEMORY_THRESHOLD = 80.0

# Путь к ансибл плейбуку
ANSIBLE_PLAYBOOK = 'playbook.yml'
ANSIBLE_INVENTORY = 'inventory'

def get_system_resources():
    # получение загрузки процессора в процентах
    cpu_output = subprocess.check_output(['top', '-b', '-n', '1'])
    cpu_line = cpu_output.decode().split('\n')[2]
#    cpu_usage_str = cpu_line.split()[1]
    cpu_usage = float(cpu_usage_str)

    # получение загрузки оперативной памяти в процентах
    memory_output = subprocess.check_output(['free', '-m'])
    memory_lines = memory_output.decode().split('\n')[1:]
    memory_info = [int(x) for x in memory_lines[0].split()[1:]]
    memory_usage = 100.0 * (1 - memory_info[1] / memory_info[0])

    return cpu_usage, memory_usage

def run_ansible_playbook():
    # сбор ансибл команды
    ansible_command = [
        'ansible-playbook',
        ANSIBLE_PLAYBOOK,
        '-i',
        ANSIBLE_INVENTORY
    ]

    # запуск ансибла
    subprocess.call(ansible_command)

def monitor_system():
    while True:
        cpu_usage, memory_usage = get_system_resources()
 #       print(f"CPU usage: {cpu_usage:.2f}%, Memory usage: {memory_usage:.2f}%")

        # обновление прометеус метрик
        CPU_METRIC.set(cpu_usage)
        MEMORY_METRIC.set(memory_usage)

        # запуск сценария ансибла если ресурсов потребляется много
        if cpu_usage > CPU_THRESHOLD or memory_usage > MEMORY_THRESHOLD:
            run_ansible_playbook()
        pbar.update(1)
        time.sleep(1) # ожидание проверки через 15 секунд

if __name__ == '__main__':
    # запуск прометеус сервера по порту 8000
    start_http_server(8000)

    # запуск
    monitor_system()
