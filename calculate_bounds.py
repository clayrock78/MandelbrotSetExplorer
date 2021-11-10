"""
* Clayton Jones * 11-9-21 *

A helper file which calculates new bounds
"""
from scipy.interpolate import interp1d
from numpy import clip


# Function definitions

def interpolate(from_point, from_lower, from_upper, into_lower, into_upper):
    function = interp1d((from_lower, from_upper), (into_lower,into_upper))
    new_point = clip(from_point, a_min=from_lower, a_max=from_upper)
    res = function(new_point)
    return float(res)

# Function calculates new bounds
def calculate(center_coordinates: tuple, current_real_bounds: tuple, current_pixel_bounds: tuple, percent_shrink: int):
    # Break center tuple into x and y coordinates
    center_x, center_y = center_coordinates

    # Break current bounds into x and y coordinates
    real_bounds_x, real_bounds_y = current_real_bounds
    pixel_bounds_x, pixel_bounds_y = current_pixel_bounds

    # Break bounds into upper and lower bounds
    real_lower_x, real_upper_x = real_bounds_x
    real_lower_y, real_upper_y = real_bounds_y

    pixel_lower_x, pixel_upper_x = pixel_bounds_x
    pixel_lower_y, pixel_upper_y = pixel_bounds_y

    fractional_shrink = percent_shrink / 100
    new_scale = (pixel_upper_x - pixel_lower_x) * fractional_shrink

    # Calculate new real boundaries
    new_pixel_lower_x = (center_x - new_scale / 2)
    new_left_bound = interpolate(new_pixel_lower_x, pixel_lower_x, pixel_upper_x, real_lower_x, real_upper_x)

    new_pixel_upper_x = (center_x + new_scale / 2)
    new_right_bound = interpolate(new_pixel_upper_x, pixel_lower_x, pixel_upper_x, real_lower_x, real_upper_x)

    new_pixel_lower_y = (center_y - new_scale / 2)
    new_bottom_bound = interpolate(new_pixel_lower_y, pixel_lower_y, pixel_upper_y, real_lower_y, real_upper_y)

    new_pixel_upper_y = (center_y + new_scale / 2)
    new_top_bound = interpolate(new_pixel_upper_y, pixel_lower_y, pixel_upper_y, real_lower_y, real_upper_y)

    # Pack new bounds into tuples
    new_real_bounds = (new_left_bound, new_right_bound), (new_bottom_bound, new_top_bound)
    new_pixel_bounds = (new_pixel_lower_x, new_pixel_upper_x), (new_pixel_lower_y, new_pixel_upper_y)
    
    return (new_real_bounds, new_pixel_bounds)
