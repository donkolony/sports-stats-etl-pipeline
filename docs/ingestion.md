# Python Ingestion Layer

To ensure the extraction code is testable, debuggable, and maintainable, the Python ingestion layer follows Clean Architecture principles, specifically focusing on the strict separation of concerns.

## Module Responsibilities

Each module has a single, distinct reason to change:

- `config.py`: Handles all configurations. It reads environment variables (like API keys) and stores constants (like the base URL for the Football-Data.org API).
- `api_client.py`: Its only job is to talk to the API. It handles authentication, makes the GET requests, and deals with pagination or rate limits. It does not know what happens to the data after it is fetched; it simply returns a Python dictionary.
- `local_storage.py`: Its only job is to interact with the file system. It takes a Python dictionary, competition code, entity and a date, constructs the `data/raw/competitions/competition_code/entity/YYYY/MM/DD/` directory path, and saves the JSON file and returns the path where the file is stored. It does not know where the data came from.
- `runner.py`: This is the orchestrator. It imports `api_client`, `local_storage`, and `duckdb_client`. It fetches the data using the client, passes it to the storage module, and immediately loads the data in the warehouse. It acts as the bridge, ensuring the client and storage never directly depend on each other.
