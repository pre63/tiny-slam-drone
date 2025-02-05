all:
	@lsof -ti:8080 | xargs kill -9 || true
	@./Llama-3.2-1B-Instruct.Q6_K.llamafile --server --v2 &
	@. .venv/bin/activate && python3 script.py api.json

install:
	@python3 -m venv .venv
	@. .venv/bin/activate && pip install --upgrade pip
	@. .venv/bin/activate && pip install -r requirements.txt
