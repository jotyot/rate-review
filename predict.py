import torch

class linearRegression(torch.nn.Module):
    def __init__(self, inputSize, outputSize):
        super(linearRegression, self).__init__()
        self.linear = torch.nn.Linear(inputSize, outputSize)

    def forward(self, x):
        out = self.linear(x)
        return out

class LinearModel:
    def __init__(self):
        self.model = linearRegression(10, 1)
        self.model.load_state_dict(torch.load('linear.pt'))
    
    def predict(self, input) -> float:
        self.model.eval()
        input_tensor = torch.tensor(input)
        with torch.no_grad():
            return self.model(input_tensor).item()
    
    def parameters(self):
        keys = ["+food", "+service", "+location", "+clean", "+price", "-food", "-service", "-location", "-clean", "-price", "bias"]
        unrounded = torch.cat([x.view(-1) for x in self.model.parameters()]).tolist()
        return {key: f'{w:.3e}' for key, w in zip(keys, unrounded)}
    
test = [1.5, 0.8333333333333334, 0.3333333333333333, 0.0, 0.16666666666666666, 0.6666666666666666, 0.0, 0.16666666666666666, 0.16666666666666666, 0.5]
model = LinearModel()
print(model.parameters())