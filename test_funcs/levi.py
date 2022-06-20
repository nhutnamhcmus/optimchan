import autograd.numpy as np
from autograd import grad
import math


class Levi:
    def __init__(self):
        super(Levi, self).__init__()
        self.xmin, self.xmax = -10, 10
        self.ymin, self.ymax = -10, 10
        self.y_start, self.x_start = -2.8, 2.4  # Start point
        self.x_optimum, self.y_optimum, self.z_optimum = 1, 1, 0  # Global optimum
        self._compute_derivatives()

    def _compute_derivatives(self):
        # Partial derivative of the objective function over x
        self.df_dx = grad(self.eval, 0)
        # Partial derivative of the objective function over y
        self.df_dy = grad(self.eval, 1)

    def eval(self, x, y):
        z = math.sin(3*math.pi*x)**2 + (x-1)**2*(1+math.sin(3*math.pi*y)
                                                 ** 2) + (y-1)**2*(1+math.sin(2*math.pi*y)**2)
        return z
