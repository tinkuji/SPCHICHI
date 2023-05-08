class Triple:
    def __init__(self, op, arg1, arg2, result):
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.result = result

    def __str__(self):
        return f"{self.result} = {self.arg1} {self.op} {self.arg2}"


class IntermediateCodeGenerator:
    def __init__(self):
        self.code = []
        self.temp_count = 0

    def new_temp(self):
        temp = f"t{self.temp_count}"
        self.temp_count += 1
        return temp

    def gen_code(self, op, arg1, arg2=None):
        result = self.new_temp()
        triple = Triple(op, arg1, arg2, result)
        self.code.append(triple)
        return result

    def print_code(self):
        for triple in self.code:
            print(triple)

    def example_code(self):
        # Example code: a = b + c * d
        a = self.gen_code("*", "c", "d")
        b = self.gen_code("+", "b", a)
        self.gen_code("=", b, "a")


# Usage
generator = IntermediateCodeGenerator()
generator.example_code()
generator.print_code()