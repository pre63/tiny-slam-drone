import brax
from brax.envs.env import Env, State
import jax.numpy as jnp
from jax import random

class DroneEnv(Env):
    def reset(self, rng: jnp.ndarray) -> State:
        # State: position (x,y,z), quaternion (w,x,y,z), velocity (x,y,z)
        qp = jnp.array([0.0, 0.0, 10.0, 1.0, 0.0, 0.0, 0.0])
        qv = jnp.zeros(3)
        info = {"status": "reset"}
        return State(qp=qp, qv=qv, info=info, reward=0.0, done=False)

    def step(self, state: State, action: jnp.ndarray) -> State:
        # Simple dynamics: add a fraction of the action to position.
        delta = action * 0.05
        new_qp = state.qp.at[0:3].add(delta)
        new_info = {"status": "stepped"}
        return State(qp=new_qp, qv=state.qv, info=new_info, reward=0.0, done=False)

def create_drone_env():
    return DroneEnv()
