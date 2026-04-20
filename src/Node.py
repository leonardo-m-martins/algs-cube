class Node(object):
    def __init__(self, pai=None, estado=None, v1=None,
                 anterior=None,  proximo=None):
        self.pai       = pai
        self.estado    = estado
        self.v1        = v1
        self.anterior  = anterior
        self.proximo   = proximo
    
    def __lt__(self, other):
        return self.v1 < other.v1

    def __gt__(self, other):
        return self.v1 > other.v1
    
    def __le__(self, other):
        return self.v1 <= other.v1
    
    def __ge__(self, other):
        return self.v1 >= other.v1
