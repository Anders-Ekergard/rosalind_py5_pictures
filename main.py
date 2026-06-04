import py5


def the_drawing(current_scale, current_symbol):
    m = 10  # Marginal
    scale = current_scale()  # Lista med 0..8 värden
    
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
            current_symbol(x, y, s)
