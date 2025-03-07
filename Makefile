run:
	uv run client.py congress/congress.py

run-wbs: 
	uv sync
	uv run wbs-main.py

tw:
	@test -f ./tailwindcss || (echo "tailwindcss binary not found! Please install from https://tailwindcss.com/blog/standalone-cli#get-started" && echo "Save binary to the root directory of this repo" && exit 1)
	./tailwindcss -i ./static/styles.css -o ./static/styles.out.css --watch
