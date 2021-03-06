from .base import Optimizer
import numpy as np

"""
The adaptive moment estimation method or Adam combine advantages of RMSProp and Adadelta, momentum. The equations applied during each iteration:
\begin{enumerate}
    \item biased decaying momentum
		\begin{equation}
			\textbf{v}^{(k+1)} = \gamma_v\textbf{v}^{(k)} + (1-\gamma_v)\textbf{g}^{(k)}
		\end{equation}

    \item biased decaying sq. gradient
	    \begin{equation}
		    \textbf{s}^{(k+1)} = \gamma_s\textbf{s}^{(k)} + (1-\gamma_s)\left(\textbf{g}^{(k)} \odot \textbf{g}^{(k)}\right)
		\end{equation}

    \item corrected decaying momentum
		\begin{equation}
			\hat{\textbf{v}}^{(k+1)} = \textbf{v}^{(k+1)} / (1-\gamma_v^k)
		\end{equation}

    \item corrected decaying sq. gradient
		\begin{equation}
			\hat{\textbf{s}}^{(k+1)} = \textbf{s}^{(k+1)} / (1-\gamma_s^k)
		\end{equation}

    \item next iterate
		\begin{equation}
			\textbf{x}^{(k+1)} = \textbf{x}^{(k)} - \alpha\hat{\textbf{v}}^{(k+1)} / \left(\epsilon + \sqrt{\hat{\textbf{s}}^{(k+1)}}\right)
		\end{equation}
\end{enumerate}
"""

class Adam(Optimizer):
    def __init__(self, cost_f, lr=0.001, beta_1=0.9, beta_2=0.999, x=None, y=None):
        super(Adam, self).__init__(cost_f, lr,
                                   x, y, beta_1=beta_1, beta_2=beta_2)
        self.m_x, self.m_y, self.v_x, self.v_y, self.t = 0, 0, 0, 0, 0

    def step(self, lr=None):
        self.t += 1
        epsilon = 1e-8
        if not lr:
            lr = self.lr
        # derivative
        f = self.cost_f.eval(self.x, self.y)
        dx = self.cost_f.df_dx(self.x, self.y)
        dy = self.cost_f.df_dy(self.x, self.y)

        self.m_x = self.beta_1*self.m_x + (1-self.beta_1)*dx
        self.m_y = self.beta_1*self.m_y + (1-self.beta_1)*dy
        self.v_x = self.beta_2*self.v_x + (1-self.beta_2)*(dx**2)
        self.v_y = self.beta_2*self.v_y + (1-self.beta_2)*(dy**2)

        m_x_hat = self.m_x/(1-self.beta_1**self.t)
        m_y_hat = self.m_y/(1-self.beta_1**self.t)
        v_x_hat = self.v_x/(1-self.beta_2**self.t)
        v_y_hat = self.v_y/(1-self.beta_2**self.t)

        self.x = self.x - (lr*m_x_hat)/(np.sqrt(v_x_hat)+epsilon)
        self.y = self.y - (lr*m_y_hat)/(np.sqrt(v_y_hat)+epsilon)
        return [self.x, self.y]
