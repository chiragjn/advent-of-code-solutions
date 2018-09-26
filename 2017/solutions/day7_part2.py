import collections
import sys

graph = collections.defaultdict(set)
node_weights = {}


def check(node, i):
    child_names, child_weights = [], []
    for child_name in graph[node]:
        imbalance_found, weight = check(child_name, i + 1)
        if imbalance_found:
            return imbalance_found, weight
        else:
            child_names.append(child_name)
            child_weights.append(weight)

    if len(set(child_weights)) > 1:
        counter = collections.Counter(child_weights)
        correct_sum = counter.most_common(1)[0][0]
        counter.pop(correct_sum)
        other_sum = counter.most_common(1)[0][0]
        imbalanced_child = child_names[child_weights.index(other_sum)]
        return True, node_weights[imbalanced_child] + (correct_sum - other_sum)

    # Uncomment for nice debug tree 
    # print(('| ' * (i)) + '-' + node + ' ' + str(sum(child_weights) + node_weights[node]))
    return False, sum(child_weights) + node_weights[node]


def main():
    global graph, node_weights
    parents = {}
    for i, line in enumerate(sys.stdin):
        parts = line.strip().split('->')
        name, weight = parts[0].strip().split()
        name = name.strip()
        weight = int(weight.rstrip(')').lstrip('('))
        node_weights[name] = weight

        if name not in parents:
            parents[name] = name

        if len(parts) > 1:
            children = set(map(str.strip, parts[1].split(', ')))
            graph[name].update(children)
            for child in children:
                parents[child] = name

    for name in parents:
        if parents[name] == name:
            root = name
            break

    solution_found, weight = check(root, 0)
    if not solution_found:
        raise ValueError('Input graph must have an imbalance')
    print(weight)


if __name__ == '__main__':
    main()
