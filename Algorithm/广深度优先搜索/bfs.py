# coding: utf-8

def bfs(graph, start, end):
    # 定义列表
    queue = []
    # f访问过得元素
    visited = set()
    queue.append([start])

    while queue:
        node = queue.pop()
        visited.add(node)

        # 取出图的子节点
        nodes = generate_related_nodes(node)

        queue.append(nodes)