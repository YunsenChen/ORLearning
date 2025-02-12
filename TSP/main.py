import numpy as np

from TspModel import TspModelInput, TspModel
from TspUtil import TspUtil

if __name__ == "__main__":
    #coordinates = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    #coordinates = TspUtil.read_tsp("data/st70.tsp")
    coordinates = TspUtil.read_tsp("data/berlin52.tsp")

    TspUtil.plot_solution(
        coordinates,
        path=None,
        title="Original data points",
        node_color='green',
        line_color='purple',
        save_path="img/Original_data_points.png"
    )

    matrix = TspUtil.convertCoordonates2Matrix(coordinates)
    # 创建输入对象
    model_input = TspModelInput(matrix)

    # 创建模型对象并求解
    tsp_model = TspModel(model_input)
    output = tsp_model.solve()
    tsp_model.model.write("solveResult/tsp_model.sol")
    # 打印结果
    output.print_result()

    TspUtil.plot_solution(
        coordinates,
        path=output.tour,
        title="COPT Solve Result",
        node_color='green',
        line_color='purple',
        save_path="img/COPT_Solve_Result.png"
    )