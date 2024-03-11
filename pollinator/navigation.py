
def calculate_move_coordinate(img_sz: tuple[float, float], to_center: tuple[float, float]):
    ia, ib = img_sz
    iac = ia / 2
    ibc = ib / 2
    ac, bc = to_center
    move_vert = iac - ac
    move_horiz = ibc - bc
    return (move_vert, move_horiz)

def calculate_move_bounds(img_sz: tuple[float, float], to_bounds: tuple[float, float, float, float]):
    a1, b1, a2, b2 = to_bounds
    ac = abs(a2 - a1) / 2
    bc = abs(b2 - b1) / 2
    center_detect = (ac + a1, bc + b1)
    return calculate_move_coordinate(img_sz, center_detect)

