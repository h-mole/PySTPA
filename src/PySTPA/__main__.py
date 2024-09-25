import argparse

from .stamp_model import STAMPModel

parser = argparse.ArgumentParser(prog="PySTPA Command line tools")
subparsers = parser.add_subparsers(dest="subcommands")
graphviz_parser = subparsers.add_parser(
    "render_graphviz", help="Convert from JSON to graphviz"
)
graphviz_parser.add_argument("--json_file", help="Path to the JSON file")
graphviz_parser.add_argument(
    "-o", "--output_graphviz_file", help="Path to the generated graphviz file"
)
# parser.
args = parser.parse_args()

if args.subcommands == "render_graphviz":
    # TODO: Implement the render_graphviz function
    STAMPModel.from_json_file(args.json_file).to_graphviz(args.output_graphviz_file)
