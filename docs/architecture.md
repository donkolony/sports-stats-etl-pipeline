## System Architecture

Our data pipeline is built around a lightweight, modern data stack for extracting, loading, and transforming Premier League football statistics. Rather than relying heavily on containers, we focus on simplicity, fast local development, and clean separation of responsibilities.

### Local Data Lake

Raw data retrieved from the **Football-Data.org API** is stored locally in a structured data lake.

Rather than placing all files into a single directory, the data is partitioned by both entity and extraction date. For example:

```text
data/
└── raw/
    └── competitions/
        └── competition_code/
            └── entity/
                └── YYYY/
                    └── MM/
                        └── DD/
```

This partitioning strategy offers several benefits:

- Makes historical backfills much easier.
- Simplifies debugging by isolating each extraction.
- Reduces the amount of data that needs to be scanned during downstream processing.

---
