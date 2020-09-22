class Helper:
    def __init__(self):
        pass

    def string_concat(self, target, tail):
        if not isinstance(target, str) or not isinstance(tail, str):
            raise TypeError("Target or tail is not string")
        target = target.split()
        target.append(tail)
        return ''.join(target)

    def make_params(self, **kwargs):
        params = {}
        for item in kwargs.items():
            #TODO: Type check?
            params[item[0]] = item[1]
        return params