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


# params = (0.2,0.1,0.1)
##################################################
# [('cat', 0.23492032289505005), ('cat', 0.14728288352489471), ('cat', 0.13097935914993286)]
# [('cat', 0.29809582233428955), ('cat', 0.2462661862373352), ('cat', 0.13935738801956177)]
test_params = [
    # [('cat', 0.3532187342643738), ('cat', 0.22708916664123535), (None, 0.11154596507549286)],0.7],
    ##################################################
    [
        [
            ("cat", 0.15381687879562378),
            ("cat", 0.14100512862205505),
            ("cat", 0.11225848644971848),
        ],
        0.7,
    ],
    # params = (0.2,0.1,0.1)
    # source = "/root/Desktop/works/pyjom/samples/image/samoyed.jpeg"
    # [('dog', 0.8835851550102234), ('dog', 0.08754527568817139), ('dog', 0.008648859336972237)]
    # source = "/root/Desktop/works/pyjom/samples/image/dog_saturday_night.jpg"
    [
        [
            (None, 0.33663231134414673),
            ("dog", 0.32254937291145325),
            ("dog", 0.0494903139770031),
        ],
        0.7,
    ],
]  # select the typical things for evaluation.
# not animal? wtf?
# source = "/root/Desktop/works/pyjom/samples/image/porn_shemale.jpeg" # definitely not animal
# [(None, 0.9894463419914246), ('dog', 1.564090962347109e-05), ('dog', 1.3550661606132053e-05)]
# source = "/root/Desktop/works/pyjom/samples/image/is_this_duck.bmp"
# [(None, 0.9864748120307922), ('dog', 1.2670795513258781e-05), (None, 9.569253961672075e-06)]
# source = "/root/Desktop/works/pyjom/samples/image/pig_really.bmp" # it's really a dog
# [(None, 0.35919442772865295), ('dog', 0.16199783980846405), ('dog', 0.07987158000469208)]
# source = "/root/Desktop/works/pyjom/samples/image/miku_on_green.png"
# besides calculating "DOG" or "CAT" we are also concerned about "NONE"
# [(None, 0.9998186230659485), (None, 1.7534730432089418e-06), (None, 7.280816021193459e-07)]
# source = "/root/Desktop/works/pyjom/samples/image/dog_with_text.jpg" # no dog
#  [(None, 0.9998675584793091), ('dog', 2.565316492564307e-07), (None, 1.562129767762599e-07)]
# source = "/root/Desktop/works/pyjom/samples/image/dog_with_text2.png" # has dog
#  [(None, 0.8876796960830688), ('dog', 0.0498274527490139), ('dog', 0.02175540290772915)]
# a little, but not focused.
# input_bias = 0.05
# skew = -0.5
# change these two things.
curve_function_kwargs = {
    "start": (0, 0),
    "end": (1, 1),
    "skew": skew,
}  # maximize the output.

from lazero.utils.logger import sprint
import hyperopt

hyperopt.hp.uniform('skew',-0.5, 0)
hyperopt.hp.uniform('input_bias',-0.5, 0)


def evaluate_params(input_bias, skew):
    difference = 0
    for subject_id,(test_param, target_output) in enumerate(test_params):
        for index, (label, confidence) in enumerate(test_param):
            scope = test_param[index:]
            scope_confidences = [elem[1] for elem in scope if elem[0] == label]
            output = multiParameterExponentialNetwork(
                *scope_confidences,
                input_bias=input_bias,
                curve_function_kwargs=curve_function_kwargs
            )
            print('test subject_id:', subject_id)
            print("label:",label)
            print("output:", output)
            print("target_output:", target_output)
            absolute_difference = abs(target_output - output)
            print("absolute difference:", absolute_difference)
            difference+=absolute_difference
            print("skew:", skew)
            sprint("input_bias:", input_bias)
    return difference
