Prototype for Actor Fault Tolerance for Ray
===========================================

- `./demo.py`: a small demo for the basic functionality.  
  The state of the counter actor is saved across multiple invocations.  
  Run with: `python3 ./demo.py`
- `./persistent_actor.py`: the implementation of the prototype.  
  This would be part of the API.
- `./benchmark_persistent_actor.py`: the benchmark code.  
  Run with (e.g.):
  - `python3 ./benchmark_persistent_actor.py --delay-ms=10`  
    The default Ray system without object reconstruction.
  - `python3 ./benchmark_persistent_actor.py --delay-ms=10 --safe-state`  
    Our prototype for persistent actor state.
  - `python3 ./benchmark_persistent_actor.py --delay-ms=10 --large`  
    Large actor state without object reconstruction.
  - `python3 ./benchmark_persistent_actor.py --delay-ms=10 --large --safe-state`  
    Large actor state with our prototype for persistent actor state.
  Let actors die during execution:
  - `python3 ./benchmark_persistent_actor.py --delay-ms=10 --failure`
  - `python3 ./benchmark_persistent_actor.py --delay-ms=10 --failure --safe-state`
  - `python3 ./benchmark_persistent_actor.py --delay-ms=10 --large --failure`
  - `python3 ./benchmark_persistent_actor.py --delay-ms=10 --large --failure --safe-state`
- `./run-benchmark.sh`: run the benchmark with some configurations.  
  Run with: `bash ./run-benchmark.sh`