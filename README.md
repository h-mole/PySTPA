# Stamp Model Creator

Create UPPAAL models from python networkx graphs.

## build pypi package

```cmd
pip install autoflake black isort pytest
pytest -s
pip install build
python3 -m build
```
## Run this package

```
pip install PySTPA

python -m PySTPA render_graphviz --json_file "../tests/assets/test.json" --output_graphviz_file out.dot
```