class FloatingPoint:
    epsilon = 1e-100

    @staticmethod
    def is_zero(value):
        return abs(value) <= FloatingPoint.epsilon