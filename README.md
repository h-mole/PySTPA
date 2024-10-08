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

This package renders a graphviz file from a json file.

Installation:

```shell
pip install PySTPA
```

A json file "docs/demo.json" is like this:

```json
{
    "controller": {
        "name": "Controller",
        "text": "Control system of plane",
        "variables": [
            "Status",
            "Check"
        ],
        "width": 3.0,
        "height": 0.8
    },
    "actuator": {
        "name": "Elevator",
        "text": "The elevator of plane",
        "width": 3.0,
        "height": 0.8
    },
    "sensor": {
        "name": "Altimeter",
        "text": "The sensor feeding back altitude",
        "width": 3.0,
        "height": 0.8
    },
    "process": {
        "name": "Plane Flying",
        "text": "The process of plane flying",
        "width": 3.0,
        "height": 0.8
    }
}
```

Just run this command:

```shell
cd docs
python -m PySTPA render_graphviz --json_file "demo.json" --output_graphviz_file demo.dot
neato.exe -Tpng -o demo.png demo.dot
```
