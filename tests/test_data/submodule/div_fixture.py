class DivFixture(object):
    def __init__(self, divisor):
        self.divisor = divisor

    def div(self, dividend):
        return self.divisor / dividend

    @staticmethod
    def random_number():
        return 4
