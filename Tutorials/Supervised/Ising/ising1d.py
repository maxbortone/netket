# Copyright 2018 The Simons Foundation, Inc. - All Rights Reserved.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import netket as nk
from mpi4py import MPI
from load_data import load

path_to_samples = 'isingsamples.txt'
path_to_targets = 'isingtargets.txt'

# Load the Hilbert space info and data 
hi, training_samples, training_targets = load(path_to_samples, path_to_targets)

# Machine

# Layers
L = 10
middle_layer_size = 20
layers = (
    nk.layer.FullyConnected(input_size=L,output_size=middle_layer_size),
    nk.layer.Tanh(input_size=middle_layer_size),
    nk.layer.FullyConnected(input_size=middle_layer_size, output_size=1),
)

ma = nk.machine.FFNN(hilbert=hi, layers=layers)
#ma = nk.machine.RbmSpin(hilbert=hi, alpha=1)
ma.init_random_parameters(seed=1234, sigma=0.001)

# Sampler
sa = nk.sampler.MetropolisLocal(machine=ma)

# Optimizer
op = nk.optimizer.Sgd(1e-2)
#op = nk.optimizer.AdaMax()

# Quantum State Reconstruction
spvsd = nk.supervised.supervised(
    sampler=sa,
    optimizer=op,
    batch_size=32,
    niter_opt=1000,
    output_file="output",
    samples=training_samples,
    targets=training_targets)

spvsd.run()
