import py5

def setup():
    py5.size(800, 500)
    py5.smooth()
    py5.no_stroke()

def draw():
    py5.background(230, 245, 255)
    py5.translate(py5.width/2, py5.height/2 + 40)
    draw_whale()

def draw_whale():
    # --- färger ---
    top_blue = py5.color(40, 90, 160)
    bottom_blue = py5.color(120, 170, 220)

    # --- kropp (bezier-form) ---
    py5.fill(top_blue)
    py5.begin_shape()
    py5.vertex(-250, 0)
    py5.bezier_vertex(-150, -120, 100, -120, 220, -10)
    py5.bezier_vertex(260, 20, 260, 80, 200, 110)
    py5.bezier_vertex(50, 160, -150, 140, -250, 40)
    py5.end_shape(py5.CLOSE)

    # --- undersida ---
    py5.fill(bottom_blue)
    py5.begin_shape()
    py5.vertex(-250, 40)
    py5.bezier_vertex(-150, 120, 50, 140, 200, 110)
    py5.bezier_vertex(150, 80, -50, 60, -250, 0)
    py5.end_shape(py5.CLOSE)

    # --- stjärtfena ---
    py5.fill(top_blue)
    py5.begin_shape()
    py5.vertex(220, -10)
    py5.bezier_vertex(260, -40, 310, -20, 330, -60)
    py5.bezier_vertex(300, -40, 260, -20, 220, 10)
    py5.end_shape(py5.CLOSE)

    # --- fena ---
    py5.begin_shape()
    py5.vertex(-50, 40)
    py5.bezier_vertex(-20, 20, 40, 40, 20, 90)
    py5.bezier_vertex(0, 70, -20, 60, -50, 40)
    py5.end_shape(py5.CLOSE)

    # --- öga ---
    py5.fill(0)
    py5.circle(-150, -10, 12)

    # --- prickar på ryggen ---
    py5.fill(255, 255, 255, 120)
    for x in range(-200, 150, 40):
        py5.circle(x, -40 - (x % 30), 6)
if __name__ == "__main__":
    py5.run_sketch()

