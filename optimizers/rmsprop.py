from .base import Optimizer
import numpy as np

"""
RMSProp extends Adagrad to avoid the effect of a monotonically decreasing learning rate.

\begin{equation}
    \hat{\textbf{s}}^{(k+1)} = \gamma\hat{\textbf{s}}^{(k)} + (1-\gamma)\left(\textbf{g}^{(k)} \odot \textbf{g}^{(k)} \right), \gamma \in [0, 1], \text{ typically close to } 0.9
\end{equation}

Update equation

\begin{equation}
    x_i^{(k+1)} = x_i^{(k)} - \frac{\alpha}{\epsilon + \sqrt{\hat{s}_i^{(k)}}}g_i^{(k)} = x_i^{(k)} - \frac{\alpha}{\epsilon + RMS(g_i)}g_i^{(k)}
\end{equation}
"""

class RMSProp(Optimizer):
    def __init__(self, cost_f, lr=0.001, decay_rate=0.9, x=None, y=None):
        super(RMSProp, self).__init__(cost_f=cost_f,
                                      lr=lr, x=x, y=y, decay_rate=decay_rate)
        self.ms_x = 0
        self.ms_y = 0

    def step(self, lr=None, decay_rate=None):
        epsilon = 1e-8
        if not lr:
            lr = self.lr
        if not decay_rate:
            decay_rate = self.decay_rate

        # Derivative
        f = self.cost_f.eval(self.x, self.y)
        dx = self.cost_f.df_dx(self.x, self.y)
        dy = self.cost_f.df_dy(self.x, self.y)

        self.ms_x = self.decay_rate * (self.ms_x) + (1-self.decay_rate)*dx**2
        self.ms_y = self.decay_rate * (self.ms_y) + (1-self.decay_rate)*dy**2

        self.x = self.x - (lr/(epsilon + np.sqrt(self.ms_x)))*dx
        self.y = self.y - (lr/(epsilon + np.sqrt(self.ms_y)))*dy

        return [self.x, self.y]
