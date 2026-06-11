import py5

def current_scale() -> list[float]:
    """Generates a list of 8 Fibonacci numbers, scaled by 0.1."""
    fib = [1, 1]
    for i in range(2, 8):  # 8 numbers: index 0-7
        fib.append(fib[i-1] + fib[i-2])
    # Scale down to fit in the window
    return [x * 2 for x in fib]  # Multiply by 2 for better visibility

def draw_circle(x, y, radius):
    """Draws a circle with given position and radius."""
    colors = [
        (226, 118, 89),  # Light brown
        (0, 92, 83),     # Dark green
    ]
    py5.push_matrix()
    py5.translate(x, y)
    py5.no_stroke()
    for i, col in enumerate(colors):
        py5.fill(*col)
        # Adjust radius to avoid overlap
        py5.circle(0, 0, radius * (0.8 - i * 0.3))
    py5.pop_matrix()

def setup():
    py5.size(750, 450)
    py5.background(255)
    py5.no_loop()  # No loop, drawing happens once

def draw():
    m = 10  # Margin
    scale = current_scale()  # 8 values

    for i in range(8):
        for j in range(8):
            # Choose scale value
            s = scale[i] if j % 2 == 0 else scale[7 - i]
            x = m + j * (py5.width / 8)
            y = m + i * (py5.height / 8)
            draw_circle(x, y, s)
if __name__=="__main__":
    py5.run_sketch()
