def unscale_points(point, width, original_dimension, height_ratio=1.5):
    height = width * height_ratio
    x, y = point
    original_width, original_height = original_dimension

    # Validate inputs for non-negative and non-zero values
    if x < 0 or y < 0:
        raise ValueError("Both x and y coordinates must be non-negative.")
    if width <= 0:
        raise ValueError("Width must be positive.")
    if height_ratio <= 0:
        raise ValueError("Height ratio must be greater than 0.")

    # Calculate the scaling factors directly from the provided dimensions
    width_scale = original_width / width
    height_scale = original_height / height

    # Unscale the point using the scaling factors
    original_x = x * width_scale
    original_y = y * height_scale

    return (original_x, original_y)
