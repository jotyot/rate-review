import torch

class linearRegression(torch.nn.Module):
    def __init__(self, inputSize, outputSize):
        super(linearRegression, self).__init__()
        self.linear = torch.nn.Linear(inputSize, outputSize)

    def forward(self, x):
        out = self.linear(x)
        if not self.training:
            out = torch.clamp(out, min=1, max=5)
        return out
    
class DynamicNN(torch.nn.Module):
    def __init__(self, input_size, hidden_size, output_size, num_hidden_layers):
        super(DynamicNN, self).__init__()
        self.input_size = input_size
        self.output_size = output_size
        self.num_hidden_layers = num_hidden_layers

        # Create the first layer
        self.layers = [torch.nn.Linear(input_size, hidden_size), torch.nn.ReLU()]

        # Create the hidden layers
        for _ in range(num_hidden_layers):
            self.layers.append(torch.nn.Linear(hidden_size, hidden_size))
            self.layers.append(torch.nn.ReLU())

        # Create the output layer
        self.layers.append(torch.nn.Linear(hidden_size, output_size))

        # Combine all layers
        self.model = torch.nn.Sequential(*self.layers)

    def forward(self, x):
        out = self.model(x)
        if not self.training:
            out = torch.clamp(out, min=1, max=5)
        return out    

class LinearModel:
    def __init__(self):
        self.model = linearRegression(10, 1)
        self.model.load_state_dict(torch.load('linear.pt'))
    
    def predict(self, input: list[float]) -> float:
        self.model.eval()
        input_tensor = torch.tensor(input)
        with torch.no_grad():
            return self.model(input_tensor).item()
    
    def parameters(self):
        keys = ["+food", "+service", "+location", "+clean", "+price", "-food", "-service", "-location", "-clean", "-price", "bias"]
        unrounded = torch.cat([x.view(-1) for x in self.model.parameters()]).tolist()
        return {key: f'{w:.3e}' for key, w in zip(keys, unrounded)}

class TotalSentNN:
    def __init__(self):
        self.model = DynamicNN(10, 40, 1, 4)
        self.model.load_state_dict(torch.load('nn4_40.pt'))
    
    def predict(self, input: list[int]) -> float:
        self.model.eval()
        input_tensor = torch.tensor(input)
        with torch.no_grad():
            return self.model(input_tensor).item()
    
test = [1.5, 0.8333333333333334, 0.3333333333333333, 0.0, 0.16666666666666666, 0.6666666666666666, 0.0, 0.16666666666666666, 0.16666666666666666, 0.5]
model = LinearModel()
print(model.parameters())