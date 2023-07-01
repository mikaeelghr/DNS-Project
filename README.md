server:
```
pip install -r requirements.txt
python server/server_setup.py
uvicorn server.server:app --host 0.0.0.0 --port 8022
```

client:
```
python client.py {your_username} {your_friend_username}
```

example:

```
:~/ python client.py client#2 client#3

send_message_to_username: client#3
message: salam mashti

:~/ python client.py client#3 client#2

send_message_to_username: client#2
message: aleyk
--- client#2 sent a message to you: salam mashti
```