

def bezier(i,depth=16,left=60,right=14,anc_x=0.5,anc_y=99):
    accur=0.0001
    def bezier_x(t):
        return 2 * anc_x * t * (1 - t) + t ** 2 
    def bezier_t(x):
        t = 0
        while t <= 1:
            if abs(bezier_x(t) - x) < accur:
                return t
            else:
                t = t + accur
    def bezier_y( t):
        return left * (1 - t) ** 2 + 2 * anc_y * t * (1 - t) + right * t ** 2
    return int(min(max(bezier_y(bezier_t(i/(2<<depth-1)))*(2<<depth-1)/100,0),2<<depth-1)+0.5)
