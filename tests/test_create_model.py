import os
from typing import cast
import networkx as nx
from PySTPA.stamp_model import STAMPModel, Controller, Actuator, Sensor, Process


def test_create_model():
    model = STAMPModel(
        controller=Controller(
            "控制器", "惯导软件，控制飞机飞向某一个坐标", ["AC", "CK"]
        ),
        actuator=Actuator("执行器", "飞机的飞控系统，控制飞机飞行"),
        process=Process("飞行过程", ""),
        sensor=Sensor("数据输入", "陀螺仪和加速度计的数据"),
    )
    model.to_graphviz("test.dot")
    print(model.to_json(ensure_ascii=False))


def test_create_from_json():
    FILE = os.path.join(os.path.dirname(__file__), "assets", "test.json")
    with open(FILE, "r", encoding="utf-8") as f:
        model = STAMPModel.from_json(f.read())
        print(model)
        model.to_graphviz("output.dot")
