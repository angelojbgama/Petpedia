import os
import re
import matplotlib.pyplot as plt
from datetime import datetime

# Caminho relativo para o arquivo de log
LOG_FILE_NAME = 'django_debug.log'
LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), LOG_FILE_NAME)

# Função para converter mtime (tempo de modificação) para datetime
def convert_mtime_to_datetime(mtime):
    return datetime.fromtimestamp(mtime)

# Função para extrair dados do log
def extract_log_data(log_file):
    timestamps = []
    file_paths = []
    messages = []
    mtime_values = []

    # Regex para identificar as entradas de log
    log_pattern = re.compile(r'(?P<level>DEBUG|INFO|WARNING|ERROR) (?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) autoreload File (?P<file_path>.+) first seen with mtime (?P<mtime>\d+\.\d+)')
    
    with open(log_file, 'r') as file:
        for line in file:
            match = log_pattern.search(line)
            if match:
                timestamp_str = match.group('timestamp')
                file_path = match.group('file_path')
                mtime = float(match.group('mtime'))
                
                # Converter timestamp para datetime
                timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S,%f')
                
                timestamps.append(timestamp)
                file_paths.append(file_path)
                mtime_values.append(mtime)
                messages.append(match.group('level'))
    
    return timestamps, file_paths, mtime_values, messages

# Função para plotar os dados
def plot_log_data(timestamps, file_paths, mtime_values, messages):
    fig, ax1 = plt.subplots(figsize=(14, 8))

    # Plotar mtime
    ax1.set_xlabel('Tempo')
    ax1.set_ylabel('Mtime (s)', color='tab:blue')
    ax1.plot(timestamps, mtime_values, 'b-', label='Mtime')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    ax1.set_title('Tempo de Modificação dos Arquivos e Tipos de Mensagens')

    # Adicionar um segundo eixo y para mensagens
    ax2 = ax1.twinx()
    colors = {'DEBUG': 'gray', 'INFO': 'blue', 'WARNING': 'orange', 'ERROR': 'red'}
    for level, color in colors.items():
        indices = [i for i, x in enumerate(messages) if x == level]
        ax2.scatter([timestamps[i] for i in indices], [mtime_values[i] for i in indices], color=color, label=level)

    ax2.set_ylabel('Níveis de Mensagem')
    ax2.tick_params(axis='y', labelcolor='tab:green')
    
    # Melhorar a visualização do eixo x
    fig.autofmt_xdate()
    fig.tight_layout()

    ax2.legend(title='Níveis de Mensagem')
    plt.show()

if __name__ == '__main__':
    timestamps, file_paths, mtime_values, messages = extract_log_data(LOG_FILE_PATH)
    plot_log_data(timestamps, file_paths, mtime_values, messages)
