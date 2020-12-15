import math

class Vector2D :
    """2 dimensional vector"""

    # Initialisierung (Constructor?)
    def __init__(self, x = 0, y = 0) :
        if type(x) in (int, float) :
            self.x = x
        else :
            return NotImplemented
        
        if type(y) in (int, float) :
            self.y = y
        else :
            return NotImplemented

    # Gleichheit (==)
    def __eq__(self, v2) :
        if type(v2) == Vector2D :
            if self.x == v2.x and self.y == v2.x :
                return True
            else :
                return False
        else :
            return NotImplemented

    # Ungleichheit (!=)
    def __ne__(self, v2) :
        return not self.__eq__(v2)

    # Größer (>)
    def __gt__(self, v2) :
        if type(v2) == Vector2D :
            return True if math.sqrt(self.x**2 + self.y**2) > math.sqrt(v2.x**2 + v2.y**2) else False
        else :
            return NotImplemented
    # Größer gleich (>=)
    def __ge__(self, v2) :
        if type(v2) == Vector2D :
            return True if math.sqrt(self.x**2 + self.y**2) >= math.sqrt(v2.x**2 + v2.y**2) else False
        else :
            return NotImplemented

    # Kleiner (<)
    def __lt__(self, v2) :
        if type(v2) == Vector2D :
            return True if math.sqrt(self.x**2 + self.y**2) < math.sqrt(v2.x**2 + v2.y**2) else False
        else :
            return NotImplemented

    # Kleiner gleich (<=)
    def __le__(self, v2) :
        if type(v2) == Vector2D :
            return True if math.sqrt(self.x**2 + self.y**2) <= math.sqrt(v2.x**2 + v2.y**2) else False
        else :
            return NotImplemented

    # Betrag des Vektors
    def magnitude(self) :
        return math.sqrt(self.x**2 + self.y**2)