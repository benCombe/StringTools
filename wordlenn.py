import numpy as np
import json
import os
import random

class WordleNN:
    def __init__(self, vocab_size, hidden_size=50, learning_rate=0.01, save_path="nn_state.json"):
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.learning_rate = learning_rate
        self.save_path = save_path
        self.hidden = None
        
        self.W1 = np.random.randn(vocab_size, self.hidden_size) * 0.01  # Input to Hidden
        self.W2 = np.random.randn(self.hidden_size, 1) * 0.01  # Hidden to Output
        
        self.load_model()
    
    def forward(self, X_subset):
        print("FORWARD")
        print(f"X_subset shape: {X_subset.shape}")
        original_size = self.W1.shape[0]  # Size expected by the network
        input_size = X_subset.shape[1]

        # If the input size is smaller than expected, pad it
        if input_size < original_size:
            padding = np.zeros((X_subset.shape[0], original_size - input_size))
            X_subset = np.hstack((X_subset, padding))  # Concatenate padding to the right

        # Perform the forward pass with the padded input
        self.hidden = np.dot(X_subset, self.W1)  # Dot product with W1
        self.hidden = np.maximum(0, self.hidden)  # ReLU activation
        output = np.dot(self.hidden, self.W2)  # Output layer
        return output
    
    def backward(self, X_subset, error):
        print("BACKWARD")
        print(f"X_subset shape: {X_subset.shape}")

        # Create a mask that identifies non-padded values (assuming padding with zeros)
        mask = X_subset != 0  # Assuming padding with zeros, adjust if different padding is used

        # Compute gradient for W2 (output layer weights)
        dW2 = np.dot(self.hidden.T, error)
        
        # Compute gradient for hidden layer (using transpose of W2)
        dHidden = np.dot(error, self.W2.T) * (self.hidden > 0)  # ReLU derivative

        # Mask the gradients with the input mask to ignore padded values
        dHidden *= mask

        # Compute gradients for W1
        dW1 = np.dot(X_subset.T, dHidden)
        
        # Update the weights
        self.W1 -= self.learning_rate * dW1
        self.W2 -= self.learning_rate * dW2
    
    #TODO FIX THIS
    def train(self, X_subset, y):
        print("TRAIN")
        print(f"X_subset shape: {X_subset.shape}")
        output = self.forward(X_subset)
        error = y - output
        print(f"Output: {output}/tError: {error}")
        print(f"Subset Length: {len(X_subset)}")
        self.backward(X_subset, error)
    
    def predict(self, X_subset):
        # Run the forward pass
        scores = self.forward(X_subset)
        # Apply a mask to ignore the padded values during prediction
        # If we padded with -1, we will not consider those features (index with -1)
        mask = X_subset != -1  # Create a mask where 1 means the feature is not padded
        # Sum up the scores only for non-padded values
        scores = scores * mask  # Element-wise multiplication to zero out padded values
        # Now select the index with the highest score from non-padded values
        return np.argmax(scores)  # Get the index with the highest score
        
    def save_model(self):
        data = {
            "W1": self.W1.tolist(),
            "W2": self.W2.tolist()
        }
        with open(self.save_path, "w") as f:
            json.dump(data, f)
        print("Model saved.")
    
    def load_model(self):
        if os.path.exists(self.save_path):
            with open(self.save_path, "r") as f:
                data = json.load(f)
                self.W1 = np.array(data["W1"])
                self.W2 = np.array(data["W2"])
            print("Model loaded from file.")
