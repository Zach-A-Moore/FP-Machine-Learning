import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import numpy as np

# 1. Load and preprocess the CSV data
def load_data(file_path):
    data = pd.read_csv(file_path)
    X = data.iloc[:, :-1].values  # Features
    y = data.iloc[:, -1].values   # Labels
    X = torch.FloatTensor(X)
    y = torch.FloatTensor(y).unsqueeze(1)
    return X, y

# 2. Define the Neural Network
class BinaryClassifier(nn.Module):
    def __init__(self, input_size):
        super(BinaryClassifier, self).__init__()
        self.layer1 = nn.Linear(input_size, 4)
        self.relu = nn.ReLU()
        self.layer2 = nn.Linear(4, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.relu(self.layer1(x))
        x = self.sigmoid(self.layer2(x))
        return x

# 3. Training function
def train_model(model, X, y, epochs=100, learning_rate=0.01):
    criterion = nn.BCELoss()
    optimizer = optim.SGD(model.parameters(), lr=learning_rate)
    
    for epoch in range(epochs):
        outputs = model(X)
        loss = criterion(outputs, y)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        if (epoch + 1) % 10 == 0:
            predictions = (outputs >= 0.5).float()
            accuracy = (predictions.eq(y).sum().item()) / y.size(0)
            print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}, Train Accuracy: {accuracy:.4f}')

# 4. Evaluation function
def evaluate_model(model, X, y, dataset_name):
    with torch.no_grad():
        outputs = model(X)
        predictions = (outputs >= 0.5).float()
        accuracy = (predictions.eq(y).sum().item()) / y.size(0)
        print(f'{dataset_name} Accuracy: {accuracy:.4f}')

# 5. Main execution
def main():
    # File paths (adjust as needed)
    datasets = {
        "Training Set": r"C:\Users\zacha\OneDrive\Desktop\FP databases\Code\NN_test\train_data.csv",
        "Test Set 1": r"C:\Users\zacha\OneDrive\Desktop\FP databases\Code\NN_test\test_data2.csv",
        "Test Set 2": r"C:\Users\zacha\OneDrive\Desktop\FP databases\Code\NN_test\test_data2.csv"
    }
    
    # Load all datasets
    data = {name: load_data(path) for name, path in datasets.items()}
    
    # Initialize model
    input_size = data["Training Set"][0].shape[1]  # Number of features
    model = BinaryClassifier(input_size)
    
    # Train on training set
    print("\nTraining on Training Set...")
    train_model(model, data["Training Set"][0], data["Training Set"][1], epochs=100, learning_rate=0.01)
    
    # Evaluate on all datasets
    print("\nEvaluating performance:")
    for name, (X, y) in data.items():
        evaluate_model(model, X, y, name)

if __name__ == "__main__":
    main()