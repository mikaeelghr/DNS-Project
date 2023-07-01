```
cd server
pip install -r requirements.txt
cd ..
python server/server_setup.py
uvicorn server.server:app --host 0.0.0.0 --port 8022
```