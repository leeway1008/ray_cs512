# ray-serve-transformers-bert

The server can be instantiated using, 

```
ray start --head
./update_model.sh
```

Requests can be send to the server using e.g.

```
python send_id_request.py
```