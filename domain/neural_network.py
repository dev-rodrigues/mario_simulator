import numpy as np


class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size, w1, w2):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        # Inicialização dos pesos
        self.W1 = w1  # np.random.randn(self.input_size, self.hidden_size)
        self.W2 = w2  # np.random.randn(self.hidden_size, self.output_size)

    def forward(self, x):
        # Cálculo da camada oculta
        self.hidden_layer = np.dot(x, self.W1)
        self.hidden_activation = self.sigmoid(self.hidden_layer)

        # Cálculo da camada de saída
        output_layer = np.dot(self.hidden_activation, self.W2)
        output_activation = self.sigmoid(output_layer)

        return output_activation

    def relu(self, x):
        return max(0, x)

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))