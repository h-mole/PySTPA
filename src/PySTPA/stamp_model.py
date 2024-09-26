from typing import Type
import networkx as nx
from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin

DEFAULT_BLOCK_HEIGHT = 0.8
DEFAULT_BLOCK_WIDTH = 3.0


class BlockCommonInterfaces:
    def get_properties(self):
        return {}

    def properties_to_label(self):
        return ""


@dataclass
class Controller(DataClassJsonMixin, BlockCommonInterfaces):
    name: str
    text: str
    variables: list[str] = field(default_factory=lambda: [])
    width: float = field(default=DEFAULT_BLOCK_WIDTH)
    height: float = field(default=DEFAULT_BLOCK_HEIGHT)

    def get_properties(self):
        return

    def properties_to_label(self):
        return "\n".join(self.variables)


@dataclass
class Actuator(DataClassJsonMixin, BlockCommonInterfaces):
    name: str
    text: str
    width: float = field(default=DEFAULT_BLOCK_WIDTH)
    height: float = field(default=DEFAULT_BLOCK_HEIGHT)


@dataclass
class Sensor(DataClassJsonMixin, BlockCommonInterfaces):
    name: str
    text: str
    width: float = field(default=DEFAULT_BLOCK_WIDTH)
    height: float = field(default=DEFAULT_BLOCK_HEIGHT)


@dataclass
class Process(DataClassJsonMixin, BlockCommonInterfaces):
    name: str
    text: str
    width: float = field(default=DEFAULT_BLOCK_WIDTH)
    height: float = field(default=DEFAULT_BLOCK_HEIGHT)


@dataclass
class Signal(DataClassJsonMixin):
    source: str
    target: str
    variables: list[str] = field(default_factory=lambda: [])


@dataclass
class STAMPModel(DataClassJsonMixin):
    controller: Controller
    actuator: Actuator
    sensor: Sensor
    process: Process
    signals: list[Signal]

    @classmethod
    def from_json_file(cls, json_file: str):
        with open(json_file, "r", encoding="utf-8") as f:
            return cls.from_json(f.read())

    def get_longest_line_num(self, lines: list[str]):
        return max(len(line.encode("utf8")) for line in lines)

    @property
    def blocks(self):
        return [self.controller, self.actuator, self.sensor, self.process]

    def to_graphviz(self, file_name: str):

        ysize = 2
        xsize = 3
        positions = {
            Controller: f"{xsize}, {ysize*2}!",
            Actuator: f"0, {ysize}!",
            Process: f"{xsize}, 0!",
            Sensor: f"{xsize*2}, {ysize}!",
        }
        self.graph = nx.DiGraph()
        FONT_NAME = "SimHei"
        self.graph.add_node("graph")
        self.graph.add_node("edge", fontname=FONT_NAME)
        self.graph.add_node("node", fontname=FONT_NAME)
        self.graph.add_nodes_from([block.name for block in self.blocks])
        aux_blocks = {
            "aux_nw": f"{0}, {ysize*2}!",
            "aux_ne": f"{xsize*2}, {ysize*2}!",
            "aux_sw": f"{0}, {0}!",
            "aux_se": f"{xsize*2}, {0}!",
        }
        controller = self.controller
        actuator = self.actuator
        sensor = self.sensor
        process = self.process
        for start, end, props in [
            (controller.name, "aux_nw", {"dir": "none"}),
            ("aux_nw", actuator.name, {}),
            (actuator.name, "aux_sw", {"dir": "none"}),
            ("aux_sw", process.name, {}),
            (process.name, "aux_se", {"dir": "none"}),
            ("aux_se", sensor.name, {}),
            (sensor.name, "aux_ne", {"dir": "none"}),
            ("aux_ne", controller.name, {}),
        ]:
            self.graph.add_edge(start, end, **props)
        print(self.signals)
        for signal in self.signals:
            if signal.source in {controller.name, process.name}:
                src, dst = list(self.graph.out_edges(signal.source))[0]
                self.graph.edges[src, dst]["label"] = "\n".join(signal.variables)
            elif signal.target in {controller.name, process.name}:
                src, dst = list(self.graph.in_edges(signal.target))[0]
                self.graph.edges[src, dst]["label"] = "\n".join(signal.variables)
            else:
                raise NotImplementedError(f"Unknown signal source or destination {signal}")
        # 插入辅助节点，用于连接控制器和传感器等，避免dot中的折线无法识别端口的问题
        for aux_block, aux_block_pos in aux_blocks.items():
            self.graph.add_node(
                aux_block,
                label="",
                pos=aux_block_pos,
                fixedsize=True,
                width=0.0,
                height=0.0,
            )
        # self.graph.add_edges_from(self.connections)
        for block in self.blocks:
            self.graph.nodes[block.name]["label"] = (
                block.__class__.__name__
                + "\n"
                + block.text
                + "\n"
                + block.properties_to_label()
            )
            self.graph.nodes[block.name]["pos"] = positions[block.__class__]
            self.graph.nodes[block.name]["shape"] = "box"
            self.graph.nodes[block.name]["fixedsize"] = True
            self.graph.nodes[block.name]["height"] = (
                block.height
                if block.height != DEFAULT_BLOCK_HEIGHT
                else len(self.graph.nodes[block.name]["label"].splitlines()) * 0.25
            )
            print(
                self.get_longest_line_num(
                    self.graph.nodes[block.name]["label"].splitlines()
                )
            )
            self.graph.nodes[block.name]["width"] = (
                block.width
                if block.width != DEFAULT_BLOCK_WIDTH
                else (
                    self.get_longest_line_num(
                        self.graph.nodes[block.name]["label"].splitlines()
                    )
                    * 14.0
                    * 0.5
                    * 1.1
                    / 72
                )
            )
        # self.grap

        P = nx.nx_pydot.to_pydot(self.graph)
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(P.to_string())
