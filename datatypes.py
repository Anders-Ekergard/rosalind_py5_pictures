# Shared domain types for the Rosalind Streams Completed Code/ folder.
#
# Anything that an algorithm or I/O parser hands around as a structured value
# can live here. Introduced in Episode 11 (Phylogenetics I):
#   * Tree    — an unrooted, undirected, edge-weighted tree with named nodes.
#   * Quartet — a bipartition of 4 species into two unordered pairs, written
#               in canonical form so equality and hashing "just work".


# A Quartet is the unordered pair-of-pairs {a, b} | {c, d}. We canonicalise
# by sorting each pair alphabetically, then ordering the two pairs by their
# first element. With that convention every quartet has exactly one
# representation, so set membership and sorting behave as expected.
Quartet = tuple[tuple[str, str], tuple[str, str]]


class Tree:
    """An undirected, edge-weighted tree with named nodes.

    Construct one via `custom_io.parse_newick`. Internally the tree is stored
    as an adjacency list: `adjacency[name]` is a list of (neighbor, weight)
    pairs, with every edge recorded in both directions. The wrapper methods
    are the intended interface for the rest of the codebase; reach for
    `adjacency` directly only when none of the methods fit.
    """

    def __init__(self, adjacency: dict[str, list[tuple[str, float]]]) -> None:
        self.adjacency = adjacency

    def neighbors(self, name: str) -> list[tuple[str, float]]:
        """The (neighbor_name, edge_weight) pairs at `name`."""
        return self.adjacency[name]

    def is_leaf(self, name: str) -> bool:
        """True iff `name` is a leaf (degree 1)."""
        return len(self.adjacency[name]) == 1

    def has(self, name: str) -> bool:
        """True iff `name` is a node of this tree."""
        return name in self.adjacency

    def leaves(self) -> list[str]:
        """All leaf names (degree-1 nodes), sorted alphabetically.

        The alphabetical order matches the column convention used by character
        tables in CTBL and the rest of the phylogenetics arc.
        """
        leaf_names: list[str] = []
        for name in self.adjacency:
            if len(self.adjacency[name]) == 1:
                leaf_names.append(name)
        leaf_names.sort()
        return leaf_names

    def edges(self) -> list[tuple[str, str, float]]:
        """Every undirected edge of the tree exactly once, as (a, b, weight).

        The adjacency list stores each edge twice (once per endpoint). This
        method walks it and emits the unordered pair the first time it sees it.
        """
        seen: set[frozenset[str]] = set()
        unique: list[tuple[str, str, float]] = []
        for a, neighbor_list in self.adjacency.items():
            for b, w in neighbor_list:
                key = frozenset((a, b))
                if key not in seen:
                    seen.add(key)
                    unique.append((a, b, w))
        return unique
