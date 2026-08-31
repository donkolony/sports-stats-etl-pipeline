.PHONY: help ingest transform build clean run-all

.DEFAULT_GOAL := help

# dbt directory flag shortcut
DBT_FLAGS := --project-dir transform --profiles-dir transform

help:
	@echo "=========================================================================="
	@echo "               Sports ETL Pipeline - Makefile Commands                	 "
	@echo "=========================================================================="
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  help    	: Show this help message"
	@echo "  ingest  	: Run the ingestion pipeline for matches, standings, and teams"
	@echo "  transform  	: Run 'dbt-build' to execute transformations and run tests"
	@echo "  run-all  	: RUn the complete pipeline (ingest -> transform)"
	@echo "  clean   	: Remove the local DuckDB warehouse files to reset the schema"
	@echo "=========================================================================="

ingest:
	@echo "Starting data ingestion..."
	uv run -m src.ingestion.runner -c PL matches
	uv run -m src.ingestion.runner -c PL standings
	uv run -m src.ingestion.runner -c PL teams
	@echo "Ingestion complete!"


transform:
	@echo "Building dbt models and excuting data quality tests..."
	uv run dbt build $(DBT_FLAGS)

build: transform

run-all: ingest transform
	@echo "End-to-end pipeline run finished successfully!"

clean:
	@echo "Cleaning up local DuckDB warehouse..."
	rm -f data/warehouse/*.db data/warehouse/*.duckdb storage/warehouse/*.db
	@echo "Warehouse reset complete."