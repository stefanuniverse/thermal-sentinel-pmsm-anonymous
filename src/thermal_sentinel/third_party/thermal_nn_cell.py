# SPDX-License-Identifier: MIT
# Copyright (c) 2021 Wilhelm Kirchgässner
# Class bodies extracted unchanged from pinned upstream notebook.
# See third_party/LICENSE-TNN and third_party/PROVENANCE.md.
from typing import List, Tuple
import numpy as np
import torch
from torch import Tensor, nn
TorchParam = nn.Parameter
target_cols = ["pm", "stator_yoke", "stator_tooth", "stator_winding"]
temperature_cols = target_cols + ["ambient", "coolant"]
input_cols = ["ambient", "coolant", "u_d", "u_q", "motor_speed", "i_d", "i_q", "i_s", "u_s"]
device = torch.device("cpu")

class DiffEqLayer(nn.Module):
    """This class is a container for the computation logic in each step.
    This layer could be used for any 'cell', also RNNs, LSTMs or GRUs."""

    def __init__(self, cell, *cell_args):
        super().__init__()
        self.cell = cell(*cell_args)

    def forward(self, input: Tensor, state: Tensor) -> Tuple[Tensor, Tensor]:
        inputs = input.unbind(0)
        outputs = torch.jit.annotate(List[Tensor], [])
        for i in range(len(inputs)):
            out, state = self.cell(inputs[i], state)
            outputs += [out]
        return torch.stack(outputs), state


class TNNCell(nn.Module):
    """The main TNN logic. Here, the sub-NNs are initialized as well as the constant learnable
    thermal capacitances. The forward function houses the LPTN ODE discretized with the explicit Euler method
    """

    def __init__(self):
        super().__init__()
        self.sample_time = 0.5  # in s
        self.output_size = len(target_cols)
        self.caps = TorchParam(torch.Tensor(self.output_size).to(device))
        nn.init.normal_(
            self.caps, mean=-9.2, std=0.5
        )  # hand-picked init mean, might be application-dependent
        n_temps = len(temperature_cols)  # number of temperatures (targets and input)
        n_conds = int(0.5 * n_temps * (n_temps - 1))  # number of thermal conductances
        # conductance net sub-NN
        self.conductance_net = nn.Sequential(
            nn.Linear(len(input_cols) + self.output_size, n_conds), nn.Sigmoid()
        )
        # populate adjacency matrix. It is used for indexing the conductance sub-NN output
        self.adj_mat = np.zeros((n_temps, n_temps), dtype=int)
        adj_idx_arr = np.ones_like(self.adj_mat)
        triu_idx = np.triu_indices(n_temps, 1)
        adj_idx_arr = adj_idx_arr[triu_idx].ravel()
        self.adj_mat[triu_idx] = np.cumsum(adj_idx_arr) - 1
        self.adj_mat += self.adj_mat.T
        self.adj_mat = torch.from_numpy(self.adj_mat[: self.output_size, :]).type(
            torch.int64
        )  # crop
        self.n_temps = n_temps

        # power loss sub-NN
        self.ploss = nn.Sequential(
            nn.Linear(len(input_cols) + self.output_size, 16),
            nn.Tanh(),
            nn.Linear(16, self.output_size),
        )

        self.temp_idcs = [i for i, x in enumerate(input_cols) if x in temperature_cols]
        self.nontemp_idcs = [
            i
            for i, x in enumerate(input_cols)
            if x not in temperature_cols + ["profile_id"]
        ]

    def forward(self, inp: Tensor, hidden: Tensor) -> Tuple[Tensor, Tensor]:
        prev_out = hidden
        temps = torch.cat([prev_out, inp[:, self.temp_idcs]], dim=1)
        sub_nn_inp = torch.cat([inp, prev_out], dim=1)
        conducts = torch.abs(self.conductance_net(sub_nn_inp))
        power_loss = torch.abs(self.ploss(sub_nn_inp))
        temp_diffs = torch.sum(
            (temps.unsqueeze(1) - prev_out.unsqueeze(-1)) * conducts[:, self.adj_mat],
            dim=-1,
        )
        out = prev_out + self.sample_time * torch.exp(self.caps) * (
            temp_diffs + power_loss
        )
        return prev_out, torch.clip(out, -1, 5)
