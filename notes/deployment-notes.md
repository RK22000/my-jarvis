# FastAPI Deployment and HTTPS Setup on Linode with DuckDNS and Nginx

---

## 1. Overview

This document outlines how to deploy a FastAPI application on a Linode server, configure a DuckDNS subdomain to point to your server, set up Nginx as a reverse proxy, and secure the connection with HTTPS using Let's Encrypt certificates via Certbot.

The architecture consists of:

- FastAPI app running locally on the server (port 8000)  
- Nginx listening on standard HTTP/HTTPS ports, reverse proxying to FastAPI  
- DuckDNS subdomain pointing to Linode public IP  
- Certbot managing free TLS certificates for HTTPS  

---

## 2. Prerequisites

- A Linode server running Ubuntu or similar Linux distribution  
- FastAPI application code ready to run locally  
- SSH access to the Linode server  
- Basic knowledge of Linux command line and text editing  
- DuckDNS account to register a free subdomain (added during this session)  

---

## 3. Domain Setup with DuckDNS (Added During This Session)

- Register a DuckDNS subdomain (e.g., `raka42.duckdns.org`) via [https://duckdns.org](https://duckdns.org)  
- Point the subdomain to your Linode server’s **public IP address**  
- DuckDNS automatically handles subdomains like `myjarvis.raka42.duckdns.org` without extra setup  
- Verify DNS resolution with `ping myjarvis.raka42.duckdns.org`  

---

## 4. Installing and Configuring Nginx Reverse Proxy

### Install Nginx

```bash
sudo apt update
sudo apt install nginx -y
```

### Create Nginx Server Block

Create a config file for your subdomain:

```bash
sudo vim /etc/nginx/sites-available/myjarvis
```

Add the following:

```nginx
server {
    listen 80;
    server_name myjarvis.raka42.duckdns.org;

    location / {
        proxy_pass http://127.0.0.1:8000;   # FastAPI app
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Enable the site and disable default

```bash
sudo ln -s /etc/nginx/sites-available/myjarvis /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
```

Test and reload Nginx

```bash
sudo nginx -t
sudo systemctl reload nginx
```

## 5. Configuring UFW Firewall

Check UFW status

```bash
sudo ufw status
```

Allow necessary ports

```bash
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
```

Verify rules

```bash
sudo ufw status
```

## 6. Deploying FastAPI App

Running with Gunicorn and Uvicorn workers

```bash
uv run gunicorn -k uvicorn.workers.UvicornWorker my_jarvis.server.app:app --bind 0.0.0.0:8000 > app.log 2>&1 &
```

This command runs your app in a production-ready way, binding to port 8000.

Logs are redirected to app.log.

Check logs via tail -f app.log.

Test local access

```bash
curl http://127.0.0.1:8000
```

## 7. Securing with HTTPS using Let's Encrypt

Install Certbot and Nginx plugin

```bash
sudo apt update
sudo apt install certbot python3-certbot-nginx -y
```

Obtain and configure SSL certificate

```bash
sudo certbot --nginx -d myjarvis.raka42.duckdns.org
```

Follow prompts to enter your email and agree to terms.

Choose to redirect all HTTP traffic to HTTPS when prompted.

Verify HTTPS access
Visit: https://myjarvis.raka42.duckdns.org

Look for the padlock icon confirming a secure connection.

Automatic renewal
Certbot sets up auto-renewal. Test it with:

```bash
sudo certbot renew --dry-run
```

## 8. Additional Tips and Next Steps

Check Nginx logs at /var/log/nginx/access.log and /var/log/nginx/error.log for troubleshooting.

Add authentication and authorization to your FastAPI endpoints for security.

Automate deploy and teardown scripts for easier management.

Consider monitoring tools and scaling options as your app grows.

## 9. Troubleshooting

If your subdomain doesn't resolve, verify DuckDNS IP update and DNS propagation.

If Nginx returns 502, check if your FastAPI app is running on port 8000.

Confirm firewall ports 22, 80, and 443 are allowed via UFW.

Use nginx -t to validate configuration syntax before reload.
