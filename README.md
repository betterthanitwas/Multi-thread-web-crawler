# Multi-thread-web-crawler
An multi threaded web crawler... It's in the name

## How do I run it?
Starting with a Google Compute Engine Ubuntu 18.04 LTS image, run these commands:
```bash
sudo apt-get update
sudo apt-get install -y mysql-server mysql-client python3 python3-pip
pip3 install beautifulsoup4 flask request mysql-connector
sudo mysql << EOF
CREATE USER 'crawl'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON * . * TO 'crawl'@'localhost';
EOF
```
(note that this is really insecure and shouldn't be used in a production setting.)

To run a crawl:
```bash
sudo mysql << EOF
DROP SCHEMA WEBCRAWL;
EOF
sudo mysql < script.sql
python3 crawl.py
```

To run the server:
```bash
python3 server.py
```
