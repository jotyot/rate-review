function LinInfo() {
  return (
    <div>
      A linear regression model that uses the weighted sentiments as its input.
      The weights of the model:
      <div className="grid grid-cols-2 text-center pt-1">
        <div className="grid grid-rows-5">
          <div>+food: 4.266e-01</div>
          <div>+service: 2.764e-01</div>
          <div>+location: 3.110e-01</div>
          <div>+clean: -7.139e-03</div>
          <div>+price: -6.851e-04</div>
        </div>
        <div className="grid grid-rows-5">
          <div>-food: -8.014e-01</div>
          <div>-service: -8.181e-01</div>
          <div>-location: -1.856e-01</div>
          <div>-clean: -6.111e-01</div>
          <div>-price: -1.680e-01</div>
        </div>
      </div>
      <div className="text-center">bias: 4.006e+00</div>
    </div>
  );
}

function NNWInfo() {
  return (
    <div>
      A neural network that uses the weighted sentiments as its input. Has a
      single hidden layer of 24 neurons.
    </div>
  );
}

function NNTInfo() {
  return (
    <div>
      A neural network that uses the total sentiments as its input. Has 4 hidden
      layers of 40 neurons each.
    </div>
  );
}

export { LinInfo, NNWInfo, NNTInfo };
