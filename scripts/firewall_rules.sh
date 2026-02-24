#!/bin/bash
# قواعد جدار الحماية المتقدمة
iptables -F
iptables -X
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# السماح للاتصالات المحلية
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# السماح للاتصالات المؤسسة
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# حماية ضد DDoS
iptables -A INPUT -p tcp --dport 80 -m limit --limit 25/minute --limit-burst 100 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -m limit --limit 25/minute --limit-burst 100 -j ACCEPT
iptables -A INPUT -p tcp --dport 5002 -m limit --limit 10/minute --limit-burst 20 -j ACCEPT

# حماية ضد Brute Force SSH
iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --set
iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --update --seconds 60 --hitcount 4 -j DROP

# رفض باقي الاتصالات
iptables -A INPUT -j DROP
