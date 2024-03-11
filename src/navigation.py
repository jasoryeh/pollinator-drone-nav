
def calculate_move_c(img_sz: tuple[float, float], to_center: tuple[float, float]):
    ia, ib = img_sz
    iac = ia / 2
    iab = ib / 2
    ac, bc = to_center
    move = "CC"
    amount = 0

    if (ac > iac):
        # to the right of screen
        if (bc > iab):
            # to the bottom of screen
            move = "LU"
            pass
        else:
            # to the top of screen
            move = "LD"
            pass
    else:
        # to the left of screen
        if (bc > iab):
            # to the bottom of screen
            move = "RU"
            pass
        else:
            # to the top of screen
            move = "RD"
            pass

    return (move, amount)

def calculate_move(img_sz: tuple[float, float], to_bounds: tuple[float, float, float, float]):
    a1, b1, a2, b2 = to_bounds
    ac = abs(a2 - a1) / 2
    bc = abs(b2 - b1) / 2

