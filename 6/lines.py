def dda(start, end, place_pixel):
    x_1, y_1 = start
    x_2, y_2 = end

    length = max(abs(x_2 - x_1), abs(y_2 - y_1))
    if length == 0:
        return

    dx = (x_2 - x_1) / length
    dy = (y_2 - y_1) / length

    x = x_1
    y = y_1

    place_pixel(*start)
    for i in range(0, length):
        x += dx
        y += dy
    place_pixel(*end)
