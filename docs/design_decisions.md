# Design Decisions

1. **Raw layer** For MagEIS data specifically, the values are all binned by energy and pitch-angle. This means at each timestamp, our measurements are in a 2d array. HAPI returns the data stored in a Numpy array. I had initially thought to store the raw layer as Parquet files, as it would flow well for our analytical use case downstream, but I would prefer to retain as much of its original representation at this stage. For this reason, I went with storing the HAPI responses as `.npz` files (a compressed set of binary `.npy` files). NPZ files also allows us to bundle in the array's metadata (shape and data type info).

    The corresponding metadata that HAPI gives comes in as dicts, so my instinct is to store them as JSON files.

    Ref: https://numpy.org/doc/stable/reference/generated/numpy.lib.format.html#npy-format
