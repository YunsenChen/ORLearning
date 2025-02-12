
from scipy.spatial.distance import pdist, squareform
import matplotlib.pyplot as plt
import numpy as np

class TspUtil:
    @staticmethod
    def read_tsp(path):
        """
        读取.tsp文件
        :return: np.array格式,nx2矩阵,其中n为点的个数,2分别为点的x与y坐标
        """
        lines = open(path, 'r').readlines()
        assert 'NODE_COORD_SECTION\n' in lines
        index = lines.index('NODE_COORD_SECTION\n')
        coordinates = []
        for line in lines[index + 1:-1]:
            line = line.strip().split(' ')
            if line[0] == 'EOF':
                break
            coordinates.append([float(line[1]), float(line[2])])
        return np.array(coordinates)

    @staticmethod
    def convertCoordonates2Matrix(coordinates):
        """
        将格式为np.array的coordinates转化为距离矩阵
        :param coordinates: 点的坐标,nx2
        :return: 距离矩阵。
        """
        # 使用pdist计算距离向量
        distances = pdist(coordinates, metric='euclidean')
        # 将向量转换为方阵形式的距离矩阵
        return squareform(distances)

    @staticmethod
    def plot_solution(coordinates, path=None, title="TSP Solution", figsize=(8, 6),
                      node_color='red', line_color='blue', show=True, save_path=None):
        """
        绘制TSP解决方案图
        :param coordinates: 初始点的坐标np.array,nx2
        :param path: 路径索引列表（可选）
        :param title: 图表标题
        :param figsize: 图表尺寸
        :param node_color: 节点颜色
        :param line_color: 路径颜色
        :param show: 是否立即显示图表
        :param save_path: 图片保存路径（可选）
        """
        plt.figure(figsize=figsize)

        # 绘制散点图
        plt.scatter(coordinates[:, 0],coordinates[:, 1], color=node_color, zorder=2)

        # 绘制路径
        if path is not None:
            TspUtil._plot_path(coordinates,path, line_color)

        plt.title(title)
        plt.xlabel("X  Coordinate")
        plt.ylabel("Y  Coordinate")
        plt.grid(True)

        # 保存或显示图表
        TspUtil._handle_output(show, save_path)
    @staticmethod
    def _plot_path(coordinates, tours, color):
        for tour in tours:
            start_point = coordinates[tour[0]]  # (565., 345.)
            end_point = coordinates[tour[1]]  # (575., 750.)
            x_coords = [start_point[0], end_point[0]]
            y_coords = [start_point[1], end_point[1]]
            plt.plot(x_coords, y_coords, color=color)

    @staticmethod
    def _handle_output(show, save_path):
        """处理图表输出"""
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        if show:
            plt.show()
        plt.close()

if __name__ == "__main__":

    coordinates = TspUtil.read_tsp("data/berlin52.tsp")

    TspUtil.plot_solution(
        coordinates,
        path=None,
        title="Random TSP Tour",
        node_color='green',
        line_color='purple',
        #save_path="tsp_solution.png"
    )

    #matrix=TspUtil.convertCoordonates2Matrix(coordinates)
