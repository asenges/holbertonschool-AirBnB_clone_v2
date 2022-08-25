#!/usr/bin/env bash
# 0. Prepare your web servers
sudo apt update
sudo apt -y install nginx
sudo mkdir -p /data/web_static/shared
sudo mkdir -p /data/web_static/releases/test
sudo echo -e "<html>\n<head>\n</head>\n<body>\nHolberton School\n</body>\n</html>" | sudo tee -a /data/web_static/releases/test/index.html
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/
sudo chmod -R 755 /data/
sudo sed -i '/\tserver_name _;/a \\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}' /etc/nginx/sites-available/default
sudo service nginx restart
