import os

from datatypes import Tree, Quartet


def read_dataset(caller_file):
    """Read dataset.txt from the same directory as the calling script."""
    directory = os.path.dirname(os.path.abspath(caller_file))
    filepath = os.path.join(directory, "dataset.txt")
    with open(filepath) as f:
        return f.read().strip()


def write_result(caller_file, result):
    """Write result to output.txt in the same directory as the calling script."""
    directory = os.path.dirname(os.path.abspath(caller_file))
    filepath = os.path.join(directory, "output.txt")
    with open(filepath, "w") as f:
        f.write(str(result) + "\n")


def parse_two_ints(caller_file):
    """Parse two integers from one line (e.g., fib, fibd datasets)."""
    text = read_dataset(caller_file)
    a, b = text.split()
    return int(a), int(b)


def parse_int(caller_file):
    """Parse a single integer (e.g., perm, sign datasets)."""
    text = read_dataset(caller_file)
    return int(text)


def parse_alphabet_and_int(caller_file):
    """Parse an alphabet (line 1) and an integer (line 2) (e.g., lexf, lexv datasets)."""
    text = read_dataset(caller_file)
    lines = text.split("\n")
    alphabet = lines[0].split()
    n = int(lines[1])
    return alphabet, n


def parse_fasta(caller_file: str) -> list[tuple[str, str]]:
    """Parse a FASTA-formatted dataset.txt from the same directory as the calling script.

    Args:
        caller_file: The __file__ variable of the calling script.

    Returns:
        A list of (label, sequence) tuples, one per FASTA record.
    """
    text = read_dataset(caller_file)
    sequences: list[tuple[str, str]] = []
    label: str | None = None
    seq_parts: list[str] = []

    for line in text.split("\n"):
        if line.startswith(">"):
            if label is not None:
                sequences.append((label, "".join(seq_parts)))
            label = line[1:]
            seq_parts = []
        else:
            seq_parts.append(line)

    if label is not None:
        sequences.append((label, "".join(seq_parts)))

    return sequences


def parse_strings(caller_file: str) -> list[str]:
    """Parse a list of strings, one per line, from dataset.txt.

    Args:
        caller_file: The __file__ variable of the calling script.

    Returns:
        A list of strings, one per line.
    """
    text = read_dataset(caller_file)
    return text.split("\n")


def parse_ints(caller_file: str) -> list[int]:
    """Parse a single line of space-separated integers from dataset.txt.

    Args:
        caller_file: The __file__ variable of the calling script.

    Returns:
        A list of integers.
    """
    text = read_dataset(caller_file)
    result = []
    for token in text.split():
        result.append(int(token))
    return result


def parse_taxa_and_character_table(caller_file: str) -> tuple[list[str], list[str]]:
    """Parse a QRT-style dataset into a taxon list and a character table.

    Dataset layout:
        line 1   integer n (we infer this from the taxon line and ignore it)
        line 2   n whitespace-separated taxon names
        line 3+  one binary character row per line (each of length n)

    Args:
        caller_file: The __file__ variable of the calling script.

    Returns:
        A pair (taxa, character_rows), where `taxa` is the list of taxon
        names in input order and `character_rows` is the list of character
        strings (with any blank lines dropped).
    """
    text = read_dataset(caller_file)
    lines = text.strip().split("\n")
    taxa = lines[1].split()
    character_rows: list[str] = []
    for line in lines[2:]:
        stripped = line.strip()
        if stripped != "":
            character_rows.append(stripped)
    return taxa, character_rows


def format_matrix(matrix: list[list[float]], precision: int = 5) -> str:
    """Format a 2-D float matrix as space-separated rows with fixed precision.

    Args:
        matrix: A 2-D list of floats.
        precision: Number of digits after the decimal point.

    Returns:
        A multi-line string with one row per line.
    """
    output_lines: list[str] = []
    for row in matrix:
        formatted: list[str] = []
        for d in row:
            formatted.append(f"{d:.{precision}f}")
        output_lines.append(" ".join(formatted))
    return "\n".join(output_lines)


def format_set(s: set[int]) -> str:
    """Format an integer set as Rosalind set notation, e.g. {1, 2, 3}.

    Args:
        s: A set of integers; will be printed in sorted order.

    Returns:
        The string '{x1, x2, ...}'.
    """
    parts: list[str] = []
    for x in sorted(s):
        parts.append(str(x))
    return "{" + ", ".join(parts) + "}"


def parse_set_notation(line: str) -> set[int]:
    """Parse a Rosalind set-notation string like '{1, 2, 3}' into a set of ints.

    Args:
        line: A string of the form '{a, b, c, ...}'.

    Returns:
        The corresponding set of integers.
    """
    inner = line.strip()
    inner = inner.lstrip("{").rstrip("}")
    if inner.strip() == "":
        return set()

    pieces = inner.split(",")
    result: set[int] = set()
    for piece in pieces:
        result.add(int(piece.strip()))
    return result


def parse_universe_and_two_sets(caller_file: str) -> tuple[int, set[int], set[int]]:
    """Parse a universe size n (line 1) and two sets in Rosalind set notation (lines 2, 3).

    Args:
        caller_file: The __file__ variable of the calling script.

    Returns:
        A tuple of (n, set_a, set_b).
    """
    text = read_dataset(caller_file)
    lines = text.split("\n")
    n = int(lines[0])
    a = parse_set_notation(lines[1])
    b = parse_set_notation(lines[2])
    return n, a, b


def format_sort_output(distance: int, reversals: list[tuple[int, int]]) -> str:
    """Format SORT output: distance on the first line, then one reversal per line.

    The solver works in 0-based indices; Rosalind wants 1-based output,
    so we convert each (i, j) to (i + 1, j + 1) here.

    Args:
        distance: The reversal distance.
        reversals: A list of (i, j) reversals (0-based, inclusive).

    Returns:
        The formatted output string.
    """
    lines: list[str] = []
    lines.append(str(distance))
    for i, j in reversals:
        lines.append(f"{i + 1} {j + 1}")
    return "\n".join(lines)


def format_quartet(quartet: Quartet) -> str:
    """Format a canonical quartet as '{a, b} {c, d}'.

    Args:
        quartet: A canonical Quartet (see `datatypes.Quartet`).

    Returns:
        The single-line Rosalind-format string for this quartet.
    """
    pair_a, pair_b = quartet
    return "{" + pair_a[0] + ", " + pair_a[1] + "} {" + pair_b[0] + ", " + pair_b[1] + "}"


def format_distance(x: float) -> str:
    """Print a distance as an int when it's whole-valued, otherwise as a float.

    Rosalind datasets usually use integer edge weights, so '75' reads more
    naturally than '75.0'. Non-integer distances still print as floats.

    Args:
        x: The distance value to format.

    Returns:
        A compact string representation suitable for the output file.
    """
    if x == int(x):
        return str(int(x))
    return f"{x:g}"


def parse_perm_pairs(caller_file: str) -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    """Parse pairs of permutations separated by blank lines from dataset.txt.

    Each block contains two lines of space-separated integers, the first
    permutation on the first line and the second on the second.

    Args:
        caller_file: The __file__ variable of the calling script.

    Returns:
        A list of (perm_a, perm_b) tuples.
    """
    text = read_dataset(caller_file)
    pairs: list[tuple[tuple[int, ...], tuple[int, ...]]] = []
    blocks = text.split("\n\n")
    for block in blocks:
        block_lines = block.split("\n")
        first_tokens = block_lines[0].split()
        second_tokens = block_lines[1].split()

        first: list[int] = []
        for token in first_tokens:
            first.append(int(token))

        second: list[int] = []
        for token in second_tokens:
            second.append(int(token))

        pairs.append((tuple(first), tuple(second)))
    return pairs


def parse_two_perms(caller_file: str) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Parse two permutations (one per line) of space-separated integers from dataset.txt.

    Args:
        caller_file: The __file__ variable of the calling script.

    Returns:
        A tuple (first_perm, second_perm) of permutation tuples.
    """
    text = read_dataset(caller_file)
    lines = text.split("\n")

    first: list[int] = []
    for token in lines[0].split():
        first.append(int(token))

    second: list[int] = []
    for token in lines[1].split():
        second.append(int(token))

    return tuple(first), tuple(second)


def tokenize_newick(text: str) -> list[str]:
    """Tokenize a Newick string into a flat list of tokens.

    Token kinds:
        '(' ')' ',' ';'   structural symbols, each its own token
        ':NUMBER'         an edge weight, kept attached to its colon
        NAME              any maximal run of non-special, non-whitespace chars
    """
    tokens: list[str] = []
    i = 0
    while i < len(text):
        c = text[i]
        if c in "(),;":
            tokens.append(c)
            i = i + 1
        elif c == ":":
            j = i + 1
            while j < len(text) and (text[j].isdigit() or text[j] in ".-+eE"):
                j = j + 1
            tokens.append(text[i:j])
            i = j
        elif c.isspace():
            i = i + 1
        else:
            j = i
            while j < len(text) and text[j] not in "(),:;" and not text[j].isspace():
                j = j + 1
            tokens.append(text[i:j])
            i = j
    return tokens


def parse_newick_subtree(tokens: list[str], pos: list[int], counter: list[int],
                         adjacency: dict[str, list[tuple[str, float]]],
                         created_nodes: list[str]) -> tuple[str, float]:
    """Recursive descent helper: parse one subtree starting at tokens[pos[0]].

    `pos` and `counter` are passed as one-element lists so recursive calls can
    share the same advancing cursor and synthetic-name counter without nested
    functions.

    Returns (root_name, weight_to_parent); the caller wires the subtree into
    its parent by adding one edge (parent, root_name, weight).
    """
    if tokens[pos[0]] == "(":
        pos[0] = pos[0] + 1
        children: list[tuple[str, float]] = []
        first_child = parse_newick_subtree(tokens, pos, counter, adjacency, created_nodes)
        children.append(first_child)
        while tokens[pos[0]] == ",":
            pos[0] = pos[0] + 1
            next_child = parse_newick_subtree(tokens, pos, counter, adjacency, created_nodes)
            children.append(next_child)
        pos[0] = pos[0] + 1  # consume ')'

        # optional internal-node name (sits right after the ')')
        name = ""
        if pos[0] < len(tokens):
            next_tok = tokens[pos[0]]
            if next_tok not in (",", ")", ";") and not next_tok.startswith(":"):
                name = next_tok
                pos[0] = pos[0] + 1
        if name == "":
            name = f"_internal_{counter[0]}"
            counter[0] = counter[0] + 1

        # optional ':weight' on this node's edge to its parent
        weight = 1.0
        if pos[0] < len(tokens) and tokens[pos[0]].startswith(":"):
            weight = float(tokens[pos[0]][1:])
            pos[0] = pos[0] + 1

        created_nodes.append(name)
        if name not in adjacency:
            adjacency[name] = []
        for child_name, child_weight in children:
            adjacency[name].append((child_name, child_weight))
            adjacency[child_name].append((name, child_weight))
        return name, weight

    # otherwise this is a leaf with a name
    name = tokens[pos[0]]
    pos[0] = pos[0] + 1

    weight = 1.0
    if pos[0] < len(tokens) and tokens[pos[0]].startswith(":"):
        weight = float(tokens[pos[0]][1:])
        pos[0] = pos[0] + 1

    created_nodes.append(name)
    if name not in adjacency:
        adjacency[name] = []
    return name, weight


def parse_newick(text: str) -> Tree:
    """Parse a Newick string into a `Tree`.

    Edges that don't carry an explicit ':weight' get weight 1.0. Unnamed
    internal nodes get synthetic names ('_internal_0', '_internal_1', ...)
    so that every node has a stable handle. A trailing ';' is optional.

    Args:
        text: A Newick tree string.

    Returns:
        A `Tree` over the named nodes of the input.
    """
    cleaned = text.strip().rstrip(";").strip()
    tokens = tokenize_newick(cleaned)
    pos = [0]
    counter = [0]
    adjacency: dict[str, list[tuple[str, float]]] = {}
    created_nodes: list[str] = []
    parse_newick_subtree(tokens, pos, counter, adjacency, created_nodes)
    return Tree(adjacency)


def parse_distance_queries(caller_file: str) -> list[tuple[Tree, str, str]]:
    """Parse a NWCK/NKEW-style dataset into (Tree, name_a, name_b) queries.

    Dataset shape: one or more blocks, separated by blank lines. Each block has
    a Newick tree (possibly split across multiple lines, ending with ';') and
    one line with two whitespace-separated node names — the query is "what's
    the distance between these two nodes in this tree?". Within a block we tell
    the tree and pair lines apart by content: lines containing '(' or ')' or
    ';' belong to the Newick text; the remaining non-empty line is the pair.

    The Newick text of each block is parsed into a `Tree` here, so the calling
    problem file can stay focused on the algorithm.

    Args:
        caller_file: The __file__ variable of the calling script.

    Returns:
        A list of (tree, name_a, name_b) queries in dataset order.
    """
    text = read_dataset(caller_file)
    queries: list[tuple[Tree, str, str]] = []
    chunks = text.split("\n\n")
    for chunk in chunks:
        tree_pieces: list[str] = []
        pair_line = ""
        for line in chunk.split("\n"):
            stripped = line.strip()
            if stripped == "":
                continue
            if "(" in stripped or ")" in stripped or ";" in stripped:
                tree_pieces.append(stripped)
            else:
                pair_line = stripped
        if pair_line == "" or len(tree_pieces) == 0:
            continue
        newick_text = " ".join(tree_pieces)
        tokens = pair_line.split()
        name_a = tokens[0]
        name_b = tokens[1]
        queries.append((parse_newick(newick_text), name_a, name_b))
    return queries


def parse_string_and_floats(caller_file: str) -> tuple[str, list[float]]:
    """Parse a DNA string (line 1) and space-separated floats (line 2) from dataset.txt.

    Args:
        caller_file: The __file__ variable of the calling script.

    Returns:
        A tuple of (dna_string, list_of_floats).
    """
    text = read_dataset(caller_file)
    lines = text.split("\n")
    dna = lines[0]
    floats = []
    for token in lines[1].split():
        floats.append(float(token))
    return dna, floats
