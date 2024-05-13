from assets.color_pallet import iron_palette
def color_distance(hex1, hex2):
    # Simple RGB distance
    rgb1 = [int(hex1[i:i+2], 16) for i in range(1, len(hex1), 2)]
    rgb2 = [int(hex2[i:i+2], 16) for i in range(1, len(hex2), 2)]
    return sum((c1 - c2) ** 2 for c1, c2 in zip(rgb1, rgb2)) ** 0.5

def color_to_temperature(color,min_temp:float,max_temp:float):
    # Convert color from BGR to hex
    hex_color = '#{0:02x}{1:02x}{2:02x}'.format(color[2], color[1], color[0])

    # Find the nearest color in the palette
    closest_color = min(iron_palette, key=lambda x: color_distance(x, hex_color))
    index = iron_palette.index(closest_color)

    # Interpolate temperature
    return min_temp + (max_temp - min_temp) * (index / len(iron_palette))
