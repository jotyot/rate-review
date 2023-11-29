import torch

class linearRegression(torch.nn.Module):
    def __init__(self, inputSize, outputSize):
        super(linearRegression, self).__init__()
        self.linear = torch.nn.Linear(inputSize, outputSize)

    def forward(self, x):
        out = self.linear(x)
        return out

class linearModel:
    def __init__(self):
        self.model = linearRegression(10, 1)
        self.model.load_state_dict(torch.load('linear_model.pt'))
    
    def predict(self, input) -> float:
        self.model.eval()
        input_tensor = torch.tensor(input)
        with torch.no_grad():
            return self.model(input_tensor).item()
    
    def parameters(self):
        unrounded = torch.cat([x.view(-1) for x in self.model.parameters()]).tolist()
        return [f'{x:.3e}' for x in unrounded]
    

# test = [1.5, 0.8333333333333334, 0.3333333333333333, 0.0, 0.16666666666666666, 0.6666666666666666, 0.0, 0.16666666666666666, 0.16666666666666666, 0.5]
# model = linearModel()
# print(model.predict(test))