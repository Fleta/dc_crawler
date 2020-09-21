class String_helper:
    def __init__(self):
        pass

    def concat(self, target, tail):
        #TODO type check
        target = target.split()
        target.append(tail)
        return ''.join(target)