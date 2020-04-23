from .._C_netket.machine import *

from .abstract_machine import AbstractMachine

from .rbm import RbmSpin, RbmSpinReal, RbmSpinSymm, RbmMultiVal, RbmSpinPhase
from .jastrow import Jastrow, JastrowSymm


def _has_jax():
    try:
        import os

        os.environ["JAX_ENABLE_X64"] = "1"
        import jax

        return True
    except ImportError:
        return False


def _has_torch():
    try:
        import torch

        return True
    except ImportError:
        return False


if _has_jax():
    from .jax import *

if _has_torch():
    from .torch import Torch, TorchLogCosh, TorchView


def MPSPeriodicDiagonal(hilbert, bond_dim, symperiod=-1):
    return MPSPeriodic(hilbert, bond_dim, diag=True, symperiod=symperiod)
