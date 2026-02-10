# Karnaugh Diagrams

A Python project for generating and minimizing Boolean functions using Karnaugh maps and the Quine-McCluskey algorithm. This project demonstrates:

- Generation of truth tables for 3- and 4-variable functions  
- Karnaugh map visualization in the terminal  
- Minimization of Boolean expressions  
- Canonical forms (FND / FNC) generation  
- Automated testing and CI integration  

---

## Features

- **Karnaugh map printing** for 3 and 4 variables  
- **Boolean function minimization** using Quine-McCluskey  
- **Truth table file generation** (`truth_table.txt`)  
- **Canonical forms** (FND/FNC) calculation  
- **Automated tests** using `pytest`  
- **CI integration** via GitHub Actions  
- **Virtual environment management** using `uv`  

---

## Installation 
This project uses `uv` for virtual environment and dependency management. Make sure you have [uv](https://astral.sh/uv/) installed.
1. Clone the repository:
   ```bash
   git clone https://github.com/lucadani7/KarnaughDiagrams
   cd KarnaughDiagrams
   ```
2. Install Python and dependencies using uv:
   ```bash
   uv python install 3.11
   uv venv
   uv pip install -r pyproject.toml
   ```

---

## Usage
Run the main program using terminal with a sigma expression as input, for example:
```bash
python3 karnaugh.py "sigma(1,5,9,13)+sigma*(3,7,11,15)"
```

---

## Testing
1. Unit tests are written with pytest. To run tests:
   ```bash
   uv run pytest -v
   ```
2. Coverage can be checked with:
   ```bash
   uv run pytest --cov=logic --cov-report=term
   ```

---

## Continuous Integration
The project uses GitHub Actions to automatically run tests on every push or pull request. The CI workflow ensures:
  - Python environment setup with uv 
  - Dependencies installation  
  - Running all pytest tests  

You can see the CI status in the Actions tab of the repository.

---

## License
This project is licensed under the Apache-2.0 License.
