# swc

See [Project Brief](docs/project_brief.md).


#### Implemented
See [docs/technical_design_document_initial_rbsp_etl.md](docs/technical_design_document_initial_rbsp_etl.md).

Ingestion of RBSP-A MagEIS L3 data through HAPI API, stored as compressed .npz files as the raw layer. Metadata is stored in JSON files. Very simple implementation, everything resides in `src/etl/main.py`. 