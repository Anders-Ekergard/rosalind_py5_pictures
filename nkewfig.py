
""" 
Code using py5, Anders Ekergård
Scale: code from Rosalind problem-solving session with Phillip Compeau, Carnegie Mellon professor and Rosalind co-founder
"""

import py5
from dna import draw_dna
from datatypes import Tree
from custom_io import parse_newick, parse_distance_queries, format_distance, write_result



def setup():
    py5.size(750, 750)
    py5.background(255)
    py5.no_loop()



def path_weight(tree: Tree, start: str, end: str) -> float:
    """Sum of edge weights on the unique path between two nodes.

    BFS from `start`, carrying the running total of edge weights along the
    way. When we first reach `end`, the value of `weight_so_far[end]` is the
    sum of weights along the unique path — there's only one path in a tree,
    so BFS finds it on the first encounter.

    Args:
        tree: The Tree to walk.
        start: Source node name.
        end: Target node name.

    Returns:
        The sum of edge weights between `start` and `end`. Returns 0.0 when
        they are the same node, and -1.0 if either name isn't in the tree.
    """
    if start == end:
        return 0.0
    #make sure both nodes are in tree
    if not tree.has(start) or not tree.has(end):
        return -1.0
    # keep track of distance to each node
    weight_so_far: dict[str, float]= {start:0}

    # quees in order of discovery
    queue: list[str]= [start]
    # index to represent current element in queue
    head = 0
    while head < len(queue):
        node = queue[head] #Current node being exploarte
        head += 1 # next element in queue
        #range over neighbors of current node
        for neighbor, edge_weight in tree.neighbors(node):
            # Have I seen this neighboor before?
            if neighbor not in weight_so_far:
                #Update weight_so_far
                weight_so_far[neighbor] = weight_so_far[node] + edge_weight
                #are we finished?
                if neighbor == end:
                    return weight_so_far[neighbor]
                # if I'm here neighbor is a new node encounteed that we need to explore
                queue.append(neighbor)
                
    return -1.0


def newick_weighted_distances(queries: list[tuple[Tree, str, str]]) -> list[float]:
    """Weighted distance for each (tree, name_a, name_b) input.

    Args:
        queries: A list of (tree, name_a, name_b) triples, one per query.

    Returns:
        A list of weighted distances, one per query, in the input order.
    """
    answers = []
    for tree, name_a, name_b in queries:
        answers.append(path_weight(tree, name_a, name_b))

    return answers

def draw():
    print("Rita")
    m = 10
    queries = [
        (
            parse_newick("(
(
(
sp|P51587|BRCA2_HUMAN:0.20897,
sp|P97929|BRCA2_MOUSE:0.20931)
:0.22163,
sp|Q9W157|BRCA2_DROME:0.42375)
:0.02097,
(
sp|Q8RXD4|BRCA1_ARATH:0.36290,
sp|B6VQ60|BRCA1_CAEEL:0.34960)
:0.04972,
(
sp|P48754|BRCA1_MOUSE:0.23164,
(
sp|Q864U1|BRCA1_BOVIN:0.13552,
(
sp|P38398|BRCA1_HUMAN:0.12372,
sp|Q95153|BRCA1_CANLF:0.12977)
:0.01352)
:0.08013)
:0.14917);
Phylogram
     
Selected  0  branches with current label

        ),
    ]
    answers = newick_weighted_distances(queries)
    scale: list[float] = answers.copy()
    # Upprepa för att få 8 värden
    while len(scale) < 8:
        scale.extend(answers)
    scale = scale[:8]
    print(scale)
    for i in range(8):
        for j in range(8):

            # Välj rätt skalvärde
            if j % 2 == 0:
                s = (scale[i])
            else:
                s = (scale[7 - i])

            x = m + j * py5.width / 8
            y = m + i * py5.height / 8

            # Skicka bara talet vidare
            draw_dna(x, y, s)
            print(s)

def key_pressed():
    """Spara en bild när 's' trycks ned."""
    if py5.key == 's':
        py5.save_frame("dnatree_######.png")
    
py5.run_sketch()
