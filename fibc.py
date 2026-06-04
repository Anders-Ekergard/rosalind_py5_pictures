import py5
from main import the_drawing

def current_scale() -> list[float]:
    """Fibonacci-lista."""
    fib = [1, 1]
    for i in range(2, 10):
        current_num = fib[i-1] + fib[i-2]
        fib.append(current_num*0.1)
    return fib

def current_symbol(x, y, radius):
    """Ritar en cirkel med given position och radie."""
    colors = [
        (226, 118, 89),
        (0, 92, 83),
    ]
    py5.push_matrix()
    py5.translate(x, y)
    py5.no_stroke()
    for i, col in enumerate(colors):
        py5.fill(*col)
        py5.circle(0, 0, radius * (1 - i))
    py5.pop_matrix()


def setup():
    py5.size(750, 450)
    py5.background(255)
    py5.no_loop()
def draw():
    the_drawing(current_scale, current_symbol)  # Skicka in de lokala funktionerna

if __name__ == "__main__":
    py5.run_sketch()