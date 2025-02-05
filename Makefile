.PHONY: all simulator training controller install-simulator install-training install-controller clean-simulator clean-training clean-controller

all: simulator training controller

# Simulator module targets
simulator:
	\$(MAKE) -C simulator

install-simulator:
	\$(MAKE) -C simulator install

clean-simulator:
	\$(MAKE) -C simulator clean

# Training module targets
training:
	\$(MAKE) -C training

install-training:
	\$(MAKE) -C training install

clean-training:
	\$(MAKE) -C training clean

# Controller module targets
controller:
	\$(MAKE) -C controller

install-controller:
	\$(MAKE) -C controller build

clean-controller:
	\$(MAKE) -C controller clean

install: install-simulator install-training install-controller