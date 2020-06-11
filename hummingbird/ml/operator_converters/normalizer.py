# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import torch
from ..common._registration import register_converter


class Normalizer(torch.nn.Module):
    def __init__(self, norm, device):
        super(Normalizer, self).__init__()
        self.norm = norm

    def forward(self, x):
        if self.norm == "l1":
            return x / torch.abs(x).sum(1, keepdim=True)
        elif self.norm == "l2":
            return x / torch.pow(torch.pow(x, 2).sum(1, keepdim=True), 0.5)
        elif self.norm == "max":
            return x / torch.max(torch.abs(x), dim=1, keepdim=True)[0]
        else:
            raise RuntimeError("Unsupported norm: {0}".format(self.norm))


def convert_sklearn_normalizer(operator, device, extra_config):
    return Normalizer(operator.raw_operator.norm, device)


register_converter("SklearnNormalizer", convert_sklearn_normalizer)
