import numpy as np



def sample_mageis_raw():
    """ Mock HAPI response data for MagEIS L3 measurements. Includes time, some n-dim fields, and some 
    scalars providing magnetic field context.
    """
    n, shape = 20, (4, 5)  # Shape corresponds to time, pitch-angle, and energy 
    rand = np.random.default_rng(0)

    dtype = [
        ("Time", "S24"),
        ("FEDU_plasmagram", float, shape),
        ("FEDU_ERROR", float, shape),
        ("L_star", float),
        ("MLT", float),
    ]
    data = np.zeros(n, dtype=dtype)

    data["Time"] = [f"2013-01-01T00:{i:02d}:00.000Z".encode() for i in range(n)]
    data["FEDU_plasmagram"] = rand.uniform(1, 100, (n, *shape))
    data["FEDU_ERROR"] = rand.uniform(0.1, 1, (n, *shape))
    data["L_star"] = rand.uniform(2, 6, n)
    data["MLT"] = rand.uniform(0, 24, n)

    return data