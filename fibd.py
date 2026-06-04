import py5

#from main import the_drawing


def setup():
    py5.size(750, 450)
    py5.background(255)
    py5.no_loop()

def current_scale()->list[int]:
    """
    Compute the number of rabbit pairs alive after n months when each pair
    lives for exactly m months.

    Rabbits become mature at age 2 and produce one new pair each month
    until they die at the end of their m-th month.

    Returns:
        A list where index i holds the number of rabbit pairs alive after month i.
    """
    n = 8
    m = 3
    # T(n)=T(n-1)+T(n-2)-T(n-m-1)
    fib =[0]*(n+1)
    fib[1]=1
    for i in range(2, n+1):
        fib[i]= fib[i-1] + fib[i-2]
        #original pair
        if i == m+1:
            fib[i]-=1

        elif i >= m+1:
            fib[i] -=fib[i-m-1]

    return fib
def current_symbol(x, y, scale):
    py5.push_matrix()
    py5.translate(x, y)
    py5.scale(scale)

    # kropp
    py5.fill(255)
    py5.ellipse(0, 0, 60, 80)

    # öron
    py5.ellipse(-20, -40, 25, 50)
    py5.ellipse(20, -40, 25, 50)

    # ögon
    py5.fill(0)
    py5.ellipse(-10, -10, 10, 10)
    py5.ellipse(10, -10, 10, 10)

    # nos
    py5.fill(255)
    py5.ellipse(0, 10, 20, 20)

    py5.pop_matrix()

def draw():
    m = 10  # Marginal
    scale = current_scale()  # Lista med 0..8 värden
#    scale =[0, 1, 2, 3, 4, 5, 6, 7]   
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

#    the_drawing(current_scale, current_symbol)
if __name__ == "__setup__":
    py5.run_sketch()