- .\venv\Scripts\activate
- py -m pip install fastapi uvicorn
- py -m pip install -r requirements.txt
- uvicorn api:app --reload --port 8000
- uvicorn api:app --reload --port 7000

**docker command**
- docker ps -a
- docker run -d --name redis-container -p 6379:6379 redis:latest
-

