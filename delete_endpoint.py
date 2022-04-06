import sys
import ray
from ray import serve

ray.init(address="auto", ignore_reinit_error=True)
serve.init()
try : 
    serve.delete_endpoint("sentiment_endpoint")
except :
    pass

try : 
    serve.delete_backend("pytorch_backend")
except :
    pass
