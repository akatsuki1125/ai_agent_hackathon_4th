import os
import re

dump_dir = "net_data"
dump_files = os.listdir(dump_dir)
#print(dump_files)
#['ssh_22_full.log', 'tcp_syn_all.log', 'icmp.log', 'http_80.log']

file_path = os.path.join(dump_dir, dump_files[0])
# with open(file_path, 'r') as f:
#     for line in f:
#         print(line)
#         break

data = []
with open(file_path, 'r') as f:
    for i in range(5):
        #print(f.readline().rstrip())
        data.append(f.readline().rstrip())

#data = [d.split(' ') for d in data]
#print(data[0])


date_reg = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6})'
data_sep = []
for line in data:
    m = re.match(date_reg + r"\s+(.*)", line)
    if m:
        data_sep.append([m.group(1),m.group(2)])

#print(data_sep)
data = data_sep
data_sep = []

ip_reg = r'IP (\S+) > (\S+):'
for line in data:
    m = re.match(ip_reg + r"\s+(.*)", line[1])
    if m:
        data_sep.append([line[0], m.group(1),m.group(2),m.group(3)])
        
print(data_sep)

fields = ['Flags', 'seq', 'ack', 'win', 'options', 'length']
val_reg = r'(\d+(?::\d+)?)'
val_regs = {"seq": r"seq "+val_reg, "ack": r"ack "+val_reg, "win": r"win "+val_reg, "length": r"length "+val_reg}
flag_reg = r'Flags (\[[^\]]*\])'
options_reg = r'options (\[[^\]]*\])'

data = data_sep
records = []
record = {}

for line in data:
    record['date'] = line[0]
    record['src_ip'] = line[1]
    record['dst_ip'] = line[2]
    record['flag'] = re.search(flag_reg, line[3]).group(1)
    record['options'] = re.search(options_reg, line[3]).group(1)
    for k,v in val_regs.items():
        record[k] = re.search(v, line[3]).group(1)
        
    records.append(record)
print(records)
