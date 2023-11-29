import torch

class linearRegression(torch.nn.Module):
    def __init__(self, inputSize, outputSize):
        super(linearRegression, self).__init__()
        self.linear = torch.nn.Linear(inputSize, outputSize)

    def forward(self, x):
        out = self.linear(x)
        return out

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

model = linearRegression(10, 1)
model.load_state_dict(torch.load('linear_model.pt'))
model.eval()

def predict(input: list[float]):
    input_tensor = torch.tensor(input)
    with torch.no_grad():
        return model(input_tensor).item()

# test = [1.5, 0.8333333333333334, 0.3333333333333333, 0.0, 0.16666666666666666, 0.6666666666666666, 0.0, 0.16666666666666666, 0.16666666666666666, 0.5]
# print(predict(test))