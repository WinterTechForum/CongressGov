run-wbs: 
	uv sync
	bash .venv/bin/activate
	uv run wbs-main.py

tw:
	./webserver/tailwindcss -i ./webserver/static/styles.css -o ./webserver/static/styles.out.css

