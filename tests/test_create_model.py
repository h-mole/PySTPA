from typing import cast
import networkx as nx
from PySTPA.stamp_model import STAMPModel, Controller, Actuator, Sensor, Process


def test_create_model():
    model = STAMPModel(
        blocks=[
            Controller("控制器", "惯导软件，控制飞机飞向某一个坐标"),
            Actuator("执行器", "飞机的飞控系统，控制飞机飞行"),
            Process("飞行过程", ""),
            Sensor("数据输入", "陀螺仪和加速度计的数据"),
        ],
        connections=[
            ("控制器", "执行器"),
            ("执行器", "飞行过程"),
            ("飞行过程", "数据输入"),
            ("数据输入", "控制器"),
        ],
    )
    model.to_graphviz("test.dot")
