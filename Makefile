# Makefile

# Variables
PYTHON := python3
SCRIPT := src/main.py
TEST_SCRIPT := scripts/test.sh
OUTPUT_LOG := ping_results.log
PYCACHE := src/__pycache__

# Configurable options
COUNT ?= 4
TTL ?= 64
INTERFACE ?= enp1s0f0
TIMEOUT ?= 1
TARGET ?= google.com

# Default target
.PHONY: all
all: run

# Run the custom ping utility with default options
.PHONY: run
run:
	@echo "Running custom ping with default options..."
	sudo $(PYTHON) $(SCRIPT) $(TARGET) -c $(COUNT) -t $(TTL) -i $(INTERFACE) --timeout $(TIMEOUT)

# Run tests using test.sh
.PHONY: test
test:
	@echo "Running tests..."
	sudo bash $(TEST_SCRIPT)

# Run tests and log results to a file
.PHONY: test-log
test-log:
	@echo "Running tests and logging results to $(OUTPUT_LOG)..."
	sudo bash $(TEST_SCRIPT) | tee $(OUTPUT_LOG)

# Clean temporary files and logs
.PHONY: clean
clean:
	@echo "Cleaning up logs and temporary files..."
	rm -rf $(OUTPUT_LOG) $(PYCACHE)
	@echo "Cleanup complete!"

# Show help menu
.PHONY: help
help:
	@echo "Makefile commands for Custom Ping Utility"
	@echo "-----------------------------------------"
	@echo "make              - Run custom ping with default options"
	@echo "make run          - Run custom ping to google.com"
	@echo "make test         - Run all test cases from test.sh"
	@echo "make test-log     - Run tests and save output to ping_results.log"
	@echo "make clean        - Clean up generated logs and temporary files"
	@echo "make help         - Show this help menu"
