import numpy as np

def curve_converter(value,curve_function):
    # do bitwise operation.
    marray = None
    curve2 = zip(curve_function[:-1],curve_function[1:])

    dtype = value.dtype
    for (orig, target0), (forig,ftarget) in curve2:
        locs1 = value>orig # forget about zero.
        locs1 = locs1.astype(dtype)
        locs2 = value<=forig
        locs2 = locs2.astype(dtype)
        # new_value = locs1 and locs2
        new_value = locs1 * locs2
        mask_backup = new_value.copy()
        # print("LOCMAP:",new_value)
        # new_value = new_value.astype(dtype)
        new_value = value * new_value
        # print("MASKED VALUES:", new_value)
        new_value = new_value.astype(np.float32)

        new_value2 = (new_value-orig)/(forig-orig)
        new_diff = new_value2*(ftarget-target0)

        new_value = target0+new_diff
        new_value = new_value*mask_backup
        new_value = new_value.astype(dtype)

        if marray is None:
            marray = new_value.copy()
        else:
            # assert np.all(marray< value) # NOT RIGHT. WHERE?
            marray += new_value
        # print("INTERMEDIATES:",marray)
    return marray

if __name__ == '__main__':
    data = np.array([1,40,100,245])
    curve_function = [[0,0],[40,30],[100,50],[150,100],[255,130]]

    out = curve_converter(data,curve_function)
    print(data)
    print(out)