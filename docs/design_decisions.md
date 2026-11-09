# Design Decisions

### Initial RBSP-MagEIS ETL
1. **Chunk size** I chose to do 1-day batch extraction and writing to the raw layer. One day has roughly 7.7k observations for this dataset. In these initial stages, I find it helpful to work with smaller granularity when validating my work and just getting to know the data. As I scale things up, I imagine this batch size won't be super optimal, so this is something I will probably revisit.
2. **Raw layer** For MagEIS data specifically, the values are all binned by energy and pitch-angle. This means at each timestamp, our measurements are in a 2d array. HAPI returns the data stored in a Numpy array. I had initially thought to store the raw layer as Parquet files, as it would flow well for our analytical use case downstream, but I would prefer to retain as much of its original representation at this stage. For this reason, I went with storing the HAPI responses as `.npz` files (a compressed set of binary `.npy` files). NPZ files also allows us to bundle in the array's metadata (shape and data type info).

    The corresponding metadata that HAPI gives comes in as dicts, so my instinct is to store them as JSON files.

    Ref: https://numpy.org/doc/stable/reference/generated/numpy.lib.format.html#npy-format

3. **Parameter selection** In going through my old code, I found that I only retrieved certain MagEIS parameters ('FEDU_plasmagram' and a few other magnetic parameters). I considered also limiting the ingestion to those select few, but I am uncertain as to which parameters may actually be useful later on and I am considering the fact that the uses of this data platform isn't limited to one study, so I am opting to ingest all possible parameters.
