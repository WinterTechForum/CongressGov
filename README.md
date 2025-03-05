# MCP Client

A client implementation for MCP with Anthropic integration.

## Requirements

- Python 3.13 or higher
- [uv](https://docs.astral.sh/uv/getting-started/installation/) package manager

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone git@github.com:WinterTechForum/CongressGov.git
   cd CongressGov
   ```

2. Create and activate a virtual environment:
   ```bash
   uv venv  # Recommended
   source .venv/bin/activate  # On Unix-like systems
   # Or on Windows:
   # .venv\Scripts\activate

   # Alternatively with Python's venv module:
   # python -m venv .venv
   # source .venv/bin/activate  # On Unix-like systems
   # .venv\Scripts\activate  # On Windows
   ```

3. Install dependencies:
   ```bash
   uv sync  
   ```

4. Configure environment variables:
   - Create a `.env` file in the project root with the following content:
     ```
     ANTHROPIC_API_KEY=your_api_key_here
     ```
   - Replace `your_api_key_here` with your actual Anthropic API key
   - Add the following to `~/.zshrc`:
   ```
   CONGRESS_GOV_KEY=congress_gov_api_key
   ```
   - Replace `congress_gov_api_key` with your [Congress.gov API key](https://api.congress.gov/sign-up/)
   - Run `source ~/.zshrc` from all open terminals


5. Running:
   `uv run python client.py congress/congress.py`

   If you have a separate tools server, replace `congress/congress.py` with the location of your server

## Environment Variables

The following environment variables are required:

- `ANTHROPIC_API_KEY`: Your Anthropic API key for authentication

## Note

Make sure to keep your `.env` file secure and never commit it to version control. The repository includes a `.gitignore` file that should already exclude the `.env` file.
