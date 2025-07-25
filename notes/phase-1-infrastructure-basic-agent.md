# Phase 1: Infrastructure & Basic Agent

**Server Setup:**
    - Linode server provisioned
    - IP: 104.237.153.82
    - User: raka

This document will track progress, notes, and todos for Phase 1.

## Phase 1 Steps & Implementation Guide

1. **Server Setup**
    - Provision a cloud VM (e.g., Linode, AWS, DigitalOcean). ✅
    - Set up SSH access and basic firewall rules. ✅
    - Install Python and required system packages. ✅

2. **Basic FastAPI App**
    - Create a new Python project (use `pyproject.toml` or `requirements.txt`).
    - Install FastAPI and Uvicorn: `pip install fastapi uvicorn`
    - Scaffold a simple FastAPI app with a health check endpoint.
    - Example:
      ```python
      from fastapi import FastAPI
      app = FastAPI()

      @app.get("/health")
      def health():
          return {"status": "ok"}
      ```
    - Run locally:
      - For a simple app: `uv run uvicorn main:app --reload`
      - For the my-jarvis project structure: `uv run uvicorn my_jarvis.server.app:app --reload`
        - This command must be run from the project root directory
        - The format is `my_jarvis.server.app:app` because:
          - `my_jarvis.server.app` is the module path to our app.py
          - `:app` refers to the FastAPI instance named `app` in that file

3. **Enable HTTPS**
    - Obtain SSL certificates (use Let's Encrypt for free certs).
    - Configure Uvicorn or a reverse proxy (e.g., Nginx) to serve HTTPS traffic.
    - Example Nginx config:
      ```
      server {
          listen 443 ssl;
          server_name your_domain.com;
          ssl_certificate /etc/letsencrypt/live/your_domain.com/fullchain.pem;
          ssl_certificate_key /etc/letsencrypt/live/your_domain.com/privkey.pem;
          location / {
              proxy_pass http://localhost:8000;
          }
      }
      ```

4. **Add Extra Authorization**
    - Choose an auth method: API key, JWT, OAuth, etc.
    - For API key:
      - Generate a secret key and store securely.
      - Add a dependency to FastAPI endpoints to check for the key in headers.
      - Example:
        ```python
        from fastapi import Depends, HTTPException, Header

        API_KEY = "your-secret-key"

        def verify_key(x_api_key: str = Header(...)):
            if x_api_key != API_KEY:
                raise HTTPException(status_code=403, detail="Unauthorized")

        @app.get("/secure-endpoint")
        def secure_endpoint(dep=Depends(verify_key)):
            return {"secure": True}
        ```

5. **Testing & Monitoring**
    - Test endpoints with curl or Postman.
    - Set up basic logging (use Python logging or FastAPI middleware).
    - Consider uptime monitoring (e.g., UptimeRobot).

---

Update this doc as you complete each step or add notes.


*To be filled as development progresses.*
