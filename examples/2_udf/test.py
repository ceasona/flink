def get_ip_src(topic, line):
    import re
    pattern_ip = r'(\d{1}|[1-9]{1}\d{1}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1}|[1-9]{1}\d{1}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1}' \
                 r'|[1-9]{1}\d{1}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1}|[1-9]{1}\d{1}|1\d\d|2[0-4]\d|25[0-5])'
    pattern_time1 = '[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}'  # YYYY-mm-dd HH:MM:SS
    pattern_ip_src = rf'{pattern_time1} (?:({pattern_ip})|(\({pattern_ip}\)))'

    if topic == 'syslog-user':
        ip_src = re.search(pattern_ip_src, line, re.M | re.I) or ''
        if ip_src:
            ip_src = ip_src.group().split(' ')[2]
    else:
        ip_src = ''
    return ip_src

def get_topic(line):
    import re
    if 'IN=' in line and 'OUT=' in line and 'MAC=' in line:
        return 'syslog-iptables'
    elif '=======================================' in line or re.search(r'localhost (.+?): \[', line, re.M | re.I):
        return 'syslog-user'
    else:
        return 'syslog-system'
line = """"
98 syslog-tcp:0:98: key=None value=b'root: [ root pts/4 2020-10-26 15:06 (172.25.2.21)]# "2020-10-26 15:12:10 root pts/4 172.25.2.21 vi /etc/rsyslog.conf"'
"""
print(get_topic(line))
print(get_ip_src("syslog-user", line))