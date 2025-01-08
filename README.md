- .\venv\Scripts\activate
- py -m pip install fastapi uvicorn
- uvicorn api:app --reload

**docker command**
- docker ps -a
- docker run -d --name redis-container -p 6379:6379 redis:latest
