run-wbs: 
	uv sync
	./.venv/bin/activate
	uv run wbs-main.py

tw:
	@which tailwindcss > /dev/null 2>&1 || echo "tailwindcss binary not found! Please install from https://tailwindcss.com/blog/standalone-cli#get-started" && echo "Save binary to the root directory of this repo" && exit 1
	./webserver/tailwindcss -i ./webserver/static/styles.css -o ./webserver/static/styles.out.css

