from prometheus_client import start_http_server, Gauge
import subprocess
import yaml
import time
import os

# Определение показателей Prometheus
CPU_METRIC = Gauge('cpu_usage_percent', 'CPU usage percent')
MEMORY_METRIC = Gauge('memory_usage_percent', 'Memory usage percent')

# Определение пороговых значений ресурсов
CPU_THRESHOLD = 80.0
MEMORY_THRESHOLD = 80.0

# Путь к ансибл плейбуку
ANSIBLE_PLAYBOOK = 'playbook.yml'
ANSIBLE_PLAYBOOK2 = 'playbook2.yml'
ANSIBLE_INVENTORY = 'inventory'

#BLACKLIST = ['top', 'htop']

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def get_system_resources():
    # получение загрузки процессора в процентах
    ps_output = subprocess.check_output(['ps', '-A', '-o', '%cpu']).decode()
    cpu_usage = sum(float(x) for x in ps_output.split()[1:])
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
def run_ansible_playbook2(process):
    ansible_command = [
        'ansible-playbook',
        ANSIBLE_PLAYBOOK2,
        '-i',
        ANSIBLE_INVENTORY,
        '--extra-vars',
        f'"process1={process}"'
    ]
    subprocess.call(ansible_command)
def monitor_system():
    while True:
        cpu_usage, memory_usage = get_system_resources()
        print(f"\rCPU usage: {cpu_usage:.2f}%, Memory usage: {memory_usage:.2f}%", end='')
        # обновление прометеус метрик
        with open('/root/django/myproject/blacklist.txt', 'r') as f:
            blacklist = f.read().splitlines()
        with open('/root/django/myproject/whitelist.txt', 'r') as f:
            whitelist = f.read().splitlines()
        CPU_METRIC.set(cpu_usage)
        MEMORY_METRIC.set(memory_usage)
        if cpu_usage > CPU_THRESHOLD or memory_usage > MEMORY_THRESHOLD:
            for process in whitelist:
                if process in subprocess.check_output(['ps', 'ax']).decode():
                    print(f"Whitelisted process detected: {process}")
                    break
            else:
                run_ansible_playbook()
           # print("High resource usage detected. Killing high resource processes...")
           # run_ansible_playbook()

        for process in blacklist:
            if process in subprocess.check_output(['ps', 'ax']).decode():
                print(f"Killing blacklisted process: {process}")
                subprocess.call(['ansible-playbook', 'playbook2.yml', '--extra-vars', f'process_name={process}'])
                break

        time.sleep(10) # ожидание проверки через 15 секунд

if __name__ == '__main__':
    # запуск прометеус сервера по порту 8000
    start_http_server(8001)
    # запуск
    monitor_system()
