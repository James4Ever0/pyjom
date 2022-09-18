import numpy as np
import bezier


def bezierCurve(start=(0, 0), end=(1, 1), skew=0):
    # skew: (-0.5,0.5) otherwise this shit will look ugly.
    assert skew >= -0.5
    assert skew <= 0.5
    x_start, y_start = start
    x_end, y_end = end
    x_diff = x_end - x_start
    y_diff = y_end - y_start
    nodes1 = np.asfortranarray(
        [
            [x_start, x_diff * (0.5 + skew), x_end],
            [y_start, y_diff * (0.5 - skew), y_end],
        ]
    )
    curve1 = bezier.Curve(nodes1, degree=2)
    curve_params = {"x_start": x_start, "x_diff": x_diff, "x_end": x_end}
    return curve1, curve_params


def evaluateBezierCurve(input_value: float, curve, curve_params: dict):
    x_start = curve_params["x_start"]
    x_end = curve_params["x_end"]
    assert x_start <= input_value
    assert x_end >= input_value
    x_diff = curve_params["x_diff"]
    s = (input_value - x_start) / x_diff
    points = curve.evaluate(s)
    # we only get the single point.
    point = points.T[0]
    x, y = point
    result = y
    return result


def multiParameterExponentialNetwork(
    *args,
    input_bias=0.05,
    curve_function=bezierCurve,
    curve_function_kwargs={"start": (0, 0), "end": (1, 1), "skew": 0},
    evaluate_function=evaluateBezierCurve
):
    curve, curve_params = curve_function(**curve_function_kwargs)
    value = evaluate_function(input_bias, curve, curve_params)
    for index, input_value in enumerate(args):
        apply_list = [input_value] * (index + 1)
        for apply_item in apply_list:
            value += (1 - value) * evaluate_function(apply_item, curve, curve_params)
    return value

params = (0.2,0.1,0.1)
input_bias = 0.05
skew = -0.5
curve_function_kwargs={"start": (0, 0), "end": (1, 1), "skew": skew} # maximize the output.

output = multiParameterExponentialNetwork(*params,input_bias=input_bias,curve_function_kwargs = curve_function_kwargs)
print('output:')