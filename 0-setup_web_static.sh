#!/usr/bin/env bash
# 0. Prepare your web servers
apt update
apt -y install nginx
mkdir -p /data/web_static/shared
mkdir -p /data/web_static/releases/test
echo -e "<html>\n<head>\n</head>\n<body>\nHolberton School\n</body>\n</html>" | tee -a /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test/ /data/web_static/current
chown -R ubuntu:ubuntu /data/
chmod -R 755 /data/
sed -i '/\tserver_name _;/a \\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}' /etc/nginx/sites-available/default
service nginx restart
