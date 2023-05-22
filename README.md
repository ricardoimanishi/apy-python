# Instalação da API no Ubuntu

Abra um terminal no seu sistema Ubuntu.
Verifique se o sistema está atualizado executando os seguintes comandos:
```
sudo apt update
```
```
sudo apt upgrade
```

O Python já deve estar pré-instalado no Ubuntu. Verifique a versão do Python que está instalada usando o seguinte comando:
```
python3 --version
```
Se o Python não estiver instalado ou se você desejar instalar uma versão específica, você pode usar o gerenciador de pacotes apt para instalar o Python. O Python 3 é geralmente instalado por padrão. Para instalar o Python 3, execute o seguinte com
```
sudo apt install python3
```
Em seguida, instale o pacote python3-pip executando o seguinte comando:
```
sudo apt install python3-pip
```
Após a instalação ser concluída, você poderá usar o pip para instalar pacotes Python. Por exemplo, para instalar o Flask, execute o seguinte comando:
```
pip3 install flask
```
Você pode usar a biblioteca PyJWT para gerar e verificar tokens JWT. Execute o seguinte comando para instalar a biblioteca via pip:
```
pip install pyjwt
```

# Para instalar HTTPS com Nginx
Para instalar HTTPS em um servidor Python, você precisará configurar um servidor web adequado, como o Nginx ou o Apache, como um proxy reverso para o seu aplicativo Python. Aqui está um passo a passo básico usando o Nginx como exemplo:
```
sudo apt install nginx
```
Crie um arquivo de configuração do servidor Nginx:
Crie um novo arquivo de configuração para o seu domínio. Por exemplo:
```
sudo nano /etc/nginx/sites-available/seu_dominio.com.br.conf
```
Dentro do arquivo de configuração, adicione o seguinte conteúdo, substituindo seu_dominio pelo seu domínio real e caminho_para_seu_app pelo caminho absoluto para o seu aplicativo Python:
```
server {
    listen 80;
    server_name seu_dominio.com.br www.seu_dominio.com.br;
    
    location / {
        proxy_pass http://localhost:8000;  # Substitua a porta pelo número da porta em que seu aplicativo Python está sendo executado
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```
Habilite o arquivo de configuração do Nginx:
Crie um link simbólico para o arquivo de configuração no diretório sites-enabled:
```
sudo ln -s /etc/nginx/sites-available/seu_dominio.com.br.conf /etc/nginx/sites-enabled/
```
Verifique a configuração do Nginx:
```
sudo nginx -t
```
Utilize o Certbot com o Nginx para obter um certificado SSL e configurar redirecionamento **seu dominio já deve estar apontado para o ip do servidor
```
sudo certbot --nginx --agree-tos --redirect --hsts --staple-ocsp --email seuemail@gmail.com -d seu_dominio.com.br
```
Reinicie o Nginx para aplicar as alterações:
```
sudo systemctl restart nginx
```

Entre na pasta onde armazerará o projeto, por exemplo: /home
```
cd /home
```
Faça o clone do projeto de api
```
git clone https://github.com/ricardoimanishi/apy-python.git app_name
```
Inicie o app
```
python3 app.py
```


Dicas Opcionais

Alterar o fuso horario do servidor:
```
sudo dpkg-reconfigure tzdata
```
