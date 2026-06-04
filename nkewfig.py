import py5
import math
from custom_io import parse_newick
from nkew import newick_weighted_distances
def setup():
    py5.size(750, 450)
    py5.background(255)
    py5.no_loop()
def draw_dna(x_offset, y_offset, scale):
    num_points = 25
    amplitude = 25 * scale
    spacing = 7 * scale
    phase_shift = math.pi

    # Rita DNA-spiralen
    for i in range(num_points):
        y = y_offset + i * spacing
        x1 = x_offset + math.sin(i * 0.35) * amplitude
        x2 = x_offset + math.sin(i * 0.35 + phase_shift) * amplitude

        # Rita baspar (cirklar)
        py5.fill(150, 200, 250, 200)
        py5.no_stroke()
        py5.ellipse(x1, y, 8 * scale, 8 * scale)
        py5.ellipse(x2, y, 8 * scale, 8 * scale)

        # Rita bindningar (linjer)
        py5.stroke(100, 150, 200, 150)  # Ljusblå, genomskinlig
        py5.stroke_weight(1 * scale)
        py5.line(x1, y, x2, y)

def draw():
    m = 10
    queries = [
    (parse_newick("((((((Q9FR37:0.00000,A0A178WIS5:0.00000):0.38893,A0A1P8B760:0.38587):0.01799,((A0A7G2ENE8:0.00000,A0A178VF52:0.00207):0.00269,(A0A654FAL7:0.00242,Q9LI77:0.00317):0.00224):0.34353):0.33612,A0A097PM28:0.01805):0.00518,(Q7XJJ7:0.00000,A0A654GDY6:0.00000):0.00896):0.00816,A0A7G2FLN3:0.01678):0.00312,A0A178UH12:0.00000,A0A5S9YH71:0.00000);"), "Q9FR37", "A0A178WIS5"),
    (parse_newick("((((((Q9FR37:0.00000,A0A178WIS5:0.00000):0.38893,A0A1P8B760:0.38587):0.01799,((A0A7G2ENE8:0.00000,A0A178VF52:0.00207):0.00269,(A0A654FAL7:0.00242,Q9LI77:0.00317):0.00224):0.34353):0.33612,A0A097PM28:0.01805):0.00518,(Q7XJJ7:0.00000,A0A654GDY6:0.00000):0.00896):0.00816,A0A7G2FLN3:0.01678):0.00312,A0A178UH12:0.00000,A0A5S9YH71:0.00000);"), "A0A7G2ENE8", "A0A654FAL7"),
    
]   
    scale=[]
    for _ in range(4):

        scale.append(newick_weighted_distances(queries)+1)
    for i in range(8):
        for j in range(8):

            # Välj rätt skalvärde
            if j % 2 == 0:
                s = scale[i]
            else:
                s = scale[7 - i]

            x = m + j * py5.width / 8
            y = m + i * py5.height / 8

            # Skicka bara talet vidare
            draw_dna(x, y, s)
if __name__ == "__setup__":
    py5.run_sketch()