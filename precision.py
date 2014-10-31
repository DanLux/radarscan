#FIXME Is there another more clever way?
class FloatingPoint:
    epsilon = 1e-1000

    @staticmethod
    def is_zero(value):
        return abs(value) <= FloatingPoint.epsilon