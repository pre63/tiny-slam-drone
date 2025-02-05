.PHONY: install train clean

install:
	@echo "Setting up Python virtual environment..."
	python3 -m venv venv && . venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

train:
	. venv/bin/activate && python train.py

clean:
	rm -rf __pycache__
