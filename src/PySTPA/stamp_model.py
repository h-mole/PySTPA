from typing import Type
import networkx as nx
from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin

# from dataclasses


@dataclass
class Controller(DataClassJsonMixin):
    name: str
    text: str
    variables: list[str] = field(default_factory=lambda: [])


@dataclass
class Actuator(DataClassJsonMixin):
    name: str
    text: str


@dataclass
class Sensor(DataClassJsonMixin):
    name: str
    text: str


@dataclass
class Process(DataClassJsonMixin):
    name: str
    text: str


@dataclass
class STAMPModel(DataClassJsonMixin):
    blocks: list[Controller | Actuator | Sensor | Process]
    connections: list[tuple[str, str]]

    def get_first_block(self, type: Type):
        for block in self.blocks:
            if isinstance(block, type):
                return block

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
        self.graph.add_nodes_from([block.name for block in self.blocks])
        aux_blocks = {
            "aux_nw": f"{0}, {ysize*2}!",
            "aux_ne": f"{xsize*2}, {ysize*2}!",
            "aux_sw": f"{0}, {0}!",
            "aux_se": f"{xsize*2}, {0}!",
        }
        controller = self.get_first_block(Controller)
        actuator = self.get_first_block(Actuator)
        sensor = self.get_first_block(Sensor)
        process = self.get_first_block(Process)
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
                block.__class__.__name__ + "\n" + block.text
            )
            self.graph.nodes[block.name]["pos"] = positions[block.__class__]
            self.graph.nodes[block.name]["shape"] = "box"
            self.graph.nodes[block.name]["fixedsize"] = True
            self.graph.nodes[block.name]["width"] = 3
        nx.nx_pydot.write_dot(self.graph, file_name)
