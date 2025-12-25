import os
import re

dump_dir = "net_data"
dump_files = os.listdir(dump_dir)
file_path = os.path.join(dump_dir, dump_files[0])

read_line_size = 1000

data = []
with open(file_path, 'r') as f:
    for i in range(read_line_size):
        data.append(f.readline().rstrip())
        
date_reg = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6})'
ip_reg = r'IP (\S+) > (\S+):'
val_reg = r'(\d+(?::\d+)?)'
val_regs = {"seq": r"seq "+val_reg, "ack": r"ack "+val_reg, "win": r"win "+val_reg, "length": r"length "+val_reg}
flag_reg = r'Flags (\[[^\]]*\])'
options_reg = r'options (\[[^\]]*\])'


def extract(reg, text, field=1):
    m = re.search(reg, text)
    if m:
        return m.group(field)
    else:
        return ''

def split_ip_port(addr):
    if addr.count('.') == 4:
        return addr.rsplit('.', 1)
    else:
        return [addr, '']

records = []

for line in data:
    record = {}
    record['date'] = extract(date_reg, line)
    record['src_ip'], record['src_port'] = split_ip_port(extract(ip_reg, line, 1))
    record['dst_ip'], record['dst_port'] = split_ip_port(extract(ip_reg, line, 2))
    record['flag'] = extract(flag_reg, line)
    record['options'] = extract(options_reg, line)
    for k,v in val_regs.items():
        record[k] = extract(v, line)
        
    records.append(record)

print(records)

