# coding: utf-8

visited_set = set()
def dfs(node, visited):
    visited_set.add(node)
    for next_node in node.children():
        if not next_node in visited:
            dfs(next_node, visited_set)