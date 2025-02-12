import coptpy as cp
from coptpy import COPT


class TspModelInput:
    """输入数据类，包含距离矩阵"""

    def __init__(self, distances):
        self.distances = distances  # 距离矩阵
        self.n = len(distances)  # 城市数量


class TspModelOutput:
    """输出结果类，包含最优路径和总距离"""

    def __init__(self, tour, total_distance):
        """
        初始化TspSolution对象。

        :param tour: [(0, 2), (1, 0), (2, 4), (3, 1), (4, 3)]表示哪些边相连

        :param total_distance: float
            整个旅行路线的总距离。
        """
        self.tour = tour  # 最优路径
        self.total_distance = total_distance  # 总距离

    def print_result(self):
        """打印结果"""
        print("Optimal Tour:")
        for edge in self.tour:
            print(f"From city {edge[0]} to city {edge[1]}")
        print(f"Total distance: {self.total_distance}")


class TspModel:
    def __init__(self, model_input):
        self.input = model_input  # 输入数据

        # Create COPT model
        self.model = cp.Envr().createModel("TSP")

        self.x = {}  # 决策变量 x_ij
        self.u = {}  # 辅助变量 u_i

    def _add_variables(self):
        """添加决策变量"""
        # 添加 x_ij 变量
        for i in range(self.input.n):
            for j in range(self.input.n):
                if i != j:
                    self.x[i, j] = self.model.addVar(lb=0, ub=1, obj=0, vtype=COPT.BINARY, name=f'x_{i}_{j}')

        # 添加 u_i 变量（用于 MTZ 约束）
        for i in range(1, self.input.n):
            self.u[i] = self.model.addVar(lb=0, name=f'u_{i}', vtype=COPT.CONTINUOUS, ub=self.input.n - 1)

    def _add_constraints(self):
        """添加约束条件"""
        for i in range(self.input.n):
            # 出发一次约束
            expr_out = cp.quicksum(self.x[i, j] for j in range(self.input.n) if i != j)
            self.model.addConstr(expr_out == 1, name=f'out_{i}')

            # 到达一次约束
            expr_in = cp.quicksum(self.x[j, i] for j in range(self.input.n) if i != j)
            self.model.addConstr(expr_in == 1, name=f'in_{i}')

        bigM = self.input.n
        # 添加 MTZ 约束
        for i in range(1, self.input.n):
            for j in range(1, self.input.n):
                if i != j:
                    expr = self.u[i] - self.u[j] + bigM * self.x[i, j]
                    self.model.addConstr(expr <= bigM - 1, name=f'mtz_{i}_{j}')

    def _set_objective(self):
        """设置目标函数"""
        obj_expr = cp.quicksum(self.input.distances[i][j] * self.x[i, j]
                               for i in range(self.input.n)
                               for j in range(self.input.n)
                               if i != j)
        self.model.setObjective(obj_expr, sense=COPT.MINIMIZE)

    def solve(self):
        """求解 TSP 问题"""
        # 添加变量、约束和目标函数
        self._add_variables()
        self._add_constraints()
        self._set_objective()

        # 求解模型
        self.model.solve()

        # 提取结果
        if self.model.status == COPT.OPTIMAL:
            tour = []
            for i in range(self.input.n):
                for j in range(self.input.n):
                    if i != j and self.x[i, j].x > 0.5:  # 判断是否有边在最优解中
                        tour.append((i, j))
            total_distance = self.model.objval
            return TspModelOutput(tour, total_distance)
        else:
            raise Exception("No optimal solution found!")
