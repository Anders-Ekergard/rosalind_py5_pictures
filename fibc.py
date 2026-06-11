import py5

def current_scale() -> list[float]:
    """Genererar en lista med 8 Fibonacci-tal, skalade med 0.1."""
    fib = [1, 1]
    for i in range(2, 8):  # 8 tal: index 0-7
        fib.append(fib[i-1] + fib[i-2])
    # Skala ner för att passa i fönstret
    return [x * 2 for x in fib]  # Multiplicera med 2 för bättre synlighet

def draw_circle(x, y, radius):
    """Ritar en cirkel med given position och radie."""
    colors = [
        (226, 118, 89),  # Ljusbrun
        (0, 92, 83),     # Mörkgrön
    ]
    py5.push_matrix()
    py5.translate(x, y)
    py5.no_stroke()
    for i, col in enumerate(colors):
        py5.fill(*col)
        # Justera radien för att undvika överlapp
        py5.circle(0, 0, radius * (0.8 - i * 0.3))
    py5.pop_matrix()

def setup():
    py5.size(750, 450)
    py5.background(255)
    py5.no_loop()  # Ingen loop, ritning sker en gång

def draw():
    m = 10  # Marginal
    scale = current_scale()  # 8 värden

    for i in range(8):
        for j in range(8):
            # Välj skalvärde
            s = scale[i] if j % 2 == 0 else scale[7 - i]
            x = m + j * (py5.width / 8)
            y = m + i * (py5.height / 8)
            draw_circle(x, y, s)
if __name__=="__main__":
    py5.run_sketch()
