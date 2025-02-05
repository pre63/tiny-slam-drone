.PHONY: all install build clean run test start-airsim

all: install build

install:
	@echo "Checking for AirSim installation..."
	if ! command -v AirSimExe >/dev/null 2>&1; then \
	  echo "AirSimExe not found. Install AirSim from https://github.com/microsoft/AirSim and add it to your PATH."; \
	  exit 1; \
	else \
	  echo "AirSim detected."; \
	fi

build:
	cargo build --manifest-path Cargo.toml

clean:
	cargo clean --manifest-path Cargo.toml

run: build
	cargo run --manifest-path Cargo.toml

test:
	cargo test --manifest-path Cargo.toml

start-airsim:
	@echo "Launching AirSim..."
	./path/to/AirSimExe &
