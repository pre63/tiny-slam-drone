import jax
import brax
import numpy as np
import matplotlib.pyplot as plt
from jax import random
from flax import linen as nn
from drone_env import create_drone_env
import requests

# Define a TinyML model using Flax.
class TinyMLModel(nn.Module):
    @nn.compact
    def __call__(self, x):
        x = nn.Conv(features=16, kernel_size=(3,3), padding="SAME")(x)
        x = nn.relu(x)
        x = nn.avg_pool(x, window_shape=(2,2), strides=(2,2))
        x = nn.Conv(features=32, kernel_size=(3,3), padding="SAME")(x)
        x = nn.relu(x)
        x = nn.avg_pool(x, window_shape=(2,2), strides=(2,2))
        x = nn.Conv(features=1, kernel_size=(3,3), padding="SAME")(x)
        x = nn.sigmoid(x)
        return x

def generate_dummy_data(num_samples=1000, img_size=(64,64,3)):
    x_train = np.random.rand(num_samples, *img_size).astype(np.float32)
    y_train = np.random.rand(num_samples, img_size[0], img_size[1], 1).astype(np.float32)
    return x_train, y_train

def fetch_airsim_data():
    url = "http://localhost:41451/api/simGetImages"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    print("AirSim data fetched:", data)
    return data

def train_model():
    x_train, y_train = generate_dummy_data()
    print("Training data generated. Input shape:", x_train.shape)
    
    model = TinyMLModel()
    key = random.PRNGKey(0)
    variables = model.init(key, x_train[0:1])
    preds = model.apply(variables, x_train[0:1])
    print("Model output shape:", preds.shape)
    
    # Use the custom drone environment.
    env = create_drone_env()
    state = env.reset(key)
    print("Drone environment state:", state)
    
    # Fetch AirSim data.
    airsim_data = fetch_airsim_data()
    
    plt.imshow(preds[0,:,:,0], cmap='gray')
    plt.title("TinyML Model Output (Drone Environment)")
    plt.show()

def main():
    train_model()

if __name__ == "__main__":
    main()
