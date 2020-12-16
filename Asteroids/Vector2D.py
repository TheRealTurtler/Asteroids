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

    # Addition
    def __add__(self, v2) :
        if type(v2) == Vector2D :
            return Vector2D(self.x + v2.x, self.y + v2.y)
        else :
            return NotImplemented

    # Multiplikation (links)
    def __mult__(self, v2) :
        if type(v2) in (int, float) :
            return Vector2D(self.x * v2, self.y * v2)
        elif type(v2) == Vector2D :
            return self.x * v2.x + self.y * v2.y
        else :
            return NotImplemented

    # Multiplikation (rechts)
    def __rmult__(self, v2) :
        return self * v2

    # Subtraction
    def __sub__(self, v2) :
        return self + (v2 * -1)

    # Division (links)
    def __truediv__(self, v2) :
        if type(v2) in (int, float) and v2 != 0 :
            return Vector2D(self.x / v2, self.y / v2)
        #elif type(v2) == Vector2D :
        #    return Vector2D(self.x + v2.x, self.y + v2.y)
        else :
            return NotImplemented

    # Division (rechts)
    def __rtruediv__(self, v2) :
        return self / v2

    # Integer-Division
    def __floordiv__(self, v2) :
        if type(v2) == int and v2 != 0 :
            return Vector2D(self.x // v2, self.y // v2)
        #elif type(v2) == Vector2D :
        #    return Vector2D(self.x + v2.x, self.y + v2.y)
        else :
            return NotImplemented

    # Integer-Division (rechts)
    def __floordiv__(self, v2) :
        return self // v2

    # Konvertierung in string
    def __str__(self) :
        return str(self.x) + ", " + str(self.y)

    # Betrag des Vektors
    def magnitude(self) :
        return math.sqrt(self.x**2 + self.y**2)