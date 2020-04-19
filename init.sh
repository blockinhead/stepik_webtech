# hello.py is a module, app is a function in it
gunicorn -b 0.0.0.0:8080 hello:app &

sudo unlink /etc/nginx/sites-enabled/default
sudo ln -sf /home/box/web/etc/nginx.conf /etc/nginx/sites-enabled/conf.conf
sudo /etc/init.d/nginx restart
