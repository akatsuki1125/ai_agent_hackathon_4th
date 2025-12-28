import os
import re
from itertools import islice
from matplotlib import pyplot as plt
from datetime import datetime
from collections import Counter, defaultdict

dump_dir = "net_data_20251226_1904"
dump_files = [f for f in os.listdir(dump_dir) if os.path.isfile(os.path.join(dump_dir, f))]
dump_file = dump_files[3]
file_path = os.path.join(dump_dir, dump_file)

read_line_size = None

data = []
with open(file_path, 'r') as f:
    data = list(islice(f, read_line_size))
        
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

src_ips = [r['src_ip'] for r in records]
counts = Counter(src_ips)
top10_ip, _ = zip(*sorted(counts.items(), key=lambda x:x[1], reverse=True)[:10])

counts_by_ip = defaultdict(Counter)
for r in records:
    ip = r["src_ip"]
    if r["date"]:
        date_mins = datetime.strptime(r["date"], "%Y-%m-%d %H:%M:%S.%f").replace(second=0, microsecond=0) 
    counts_by_ip[ip][date_mins] += 1

# dates = [r['date'] for r in records if r['src_ip'] in top10_ip]
# date_mins = [datetime.strptime(r["date"], "%Y-%m-%d %H:%M:%S.%f").replace(second=0, microsecond=0) for date in dates]
# counts = Counter(date_mins)
# xs, ys = zip(*sorted(counts.items()))

plt.title(dump_file)
for ip in top10_ip:
    xs, ys = zip(*sorted(counts_by_ip[ip].items()))
    plt.plot(xs, ys,label=ip)

plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
os.makedirs(f'{dump_dir}/plots', exist_ok=True)
plt.savefig(f'{dump_dir}/plots/{dump_file}.png')