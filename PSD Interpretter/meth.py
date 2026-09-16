import math

def lerp(v0, v1, t):
    return (1 - t) * v0 + t * v1

def c8(run):
    return f"{int(lerp(0, 255, run)):02x}"

def decompose_transform_matrix_for_ass_format(transform):
    a, b, c, d, tx, ty = transform   # xx, xy, yx, yy, tx, ty

    scale_x = math.hypot(a, b)
    det = a * d - b * c
    if scale_x == 0 or det == 0:
        raise ValueError("degenerate matrix")

    scale_y = det / scale_x          # negatifse dikey flip var
    rotation = math.atan2(b, a)
    shear = (a * c + b * d) / det    # tan(skew açısı)

    return {
        "rotation_deg": round(math.degrees(-rotation), 2),
        "shear_factor": round(-shear * scale_x / scale_y, 2),
        "scale_x": round(scale_x * 100, 2),
        "scale_y": round(scale_y * 100, 2),
    }