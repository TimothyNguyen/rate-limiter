.\venv\Scripts\activate
py -m pip install fastapi uvicorn
uvicorn rate-limiter:app --reload
