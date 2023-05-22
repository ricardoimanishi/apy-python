# Instalação da API no Ubuntu

sudo apt update
sudo apt upgrade
python3 --version
sudo apt install python3-pip
pip3 install flask
pip install pyjwt
sudo apt install nginx
sudo nano /etc/nginx/sites-available/api.apidowhats.com.br.conf

```
server {
    listen 80;
    server_name api.apidowhats.com.br www.api.apidowhats.com.br;
    
    location / {
        proxy_pass http://localhost:8000;  # Substitua a porta pelo número da porta em que seu aplicativo Python está sendo executado
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

sudo ln -s /etc/nginx/sites-available/api.apidowhats.com.br.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo certbot --nginx --agree-tos --redirect --hsts --staple-ocsp --email ricardoimanishi@gmail.com -d api.apidowhats.com.br
sudo systemctl restart nginx
