# coding=utf-8
class DomainException(Exception):
    pass

class Color:
    def __init__(self):
        pass

    Red, Green, Blue = range(3)

class Variable(object):
    def __init__(self, fixed_value=None):
        # załpżono, że dziedzina dla wszystkich zmiennych jest taka sama [1..20]
        # ale równie dobrze może być przekazywana do konstruktora
        self.domain =  [Color.Red, Color.Green, Color.Blue] if fixed_value is None else [fixed_value]
        self._value = fixed_value

    # pozwala skorzystać z wbudowanej funkcji sum()
    def __radd__(self, other):
        if other is None: raise ValueError("Cannot sum None variable")
        return self.value + other

    # getter i setter dla value, rzuca wyjąktiem przy próbie przypisania
    # wartości spoza dziedziny
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if val != None and not val in self.domain:
            raise DomainException(str(val))
        self._value = val

    def __repr__(self):
        return str(self.value)

    # informacja czy jest przypisana, tj czy value != None
    @property
    def is_assigned(self):
        return self.value != None

class Assingment(object):
    # vars to lista zmiennych w problemie
    def __init__(self, vars):
        self.variables = vars

    # czy wszystkie zmienne mają wartość?
    def is_complete(self):
        not_assigned = [x for x in self.variables if x.value == None]
        return not not_assigned

    # weź pierwszą nieprzypisaną, jeśli takich nie ma rzuć wyjątek
    def get_unassigned_variable(self):
        for v in self.variables:
            if not v.is_assigned:
                return v
        raise AssertionError()

    # pokaż na ekranie w sensownym formacie
    def pretty_print(self):
        for i in range(0,4):
            print ' '.join(str(self.variables[i*4:i*4+4]))



class MagicSquare(object):
    def __init__(self):
        self.summary = 34 # suma kwadratu
        self.square_size = 4 # rozmiar kwadratu
        self.XD = Variable(None)
        self.WA = Variable(None)
        self.NT = Variable(None)
        self.ST = Variable(None)
        self.Q = Variable(None)
        self.NSA = Variable(None)
        self.V = Variable(None)
        self.T = Variable(None)
        self.DD = Variable(None)

    # mały helper aby łątwiej tworzyć listę zmiennych z podanych wartości
    # więcej na temat tej składni można znaleźć pod hasłem list comprehension
    def get_variables_from_values(self, values):
        return [Variable(x) for x in values]

    # początkowe wartości zmiennych. Liczby oznaczają stałą wartość, None to miejsca
    # do których ma wstawić algorytm
    def get_initial_assignment(self):
        return Assingment([self.XD, self.WA ,self.NT ,self.ST ,self.Q  , self.NSA,self.V, self.T, self.DD  ])

    def edge_invalid(self, a, b):
        if not a.is_assigned or not b.is_assigned:
            return False

        return a.value == b.value


    # sprawdza czy podstawienie narusza ograniczenia
    def is_violating_constraints(self,xd, wa, nt, st, q, nsa, v, t, dd):
        #alias coby mniej pisać ;)

        if self.edge_invalid(wa, nt): return True
        if self.edge_invalid(wa, st): return True
        if self.edge_invalid(st, nt): return True
        if self.edge_invalid(q, nt): return True
        if self.edge_invalid(st, nsa): return True
        if self.edge_invalid(q, nsa): return True
        if self.edge_invalid(v, nsa): return True
        if self.edge_invalid(st, v): return True

        if self.edge_invalid(xd, wa): return True
        #if self.edge_invalid(xd, nt): return True
        if self.edge_invalid(xd, st): return True


        if self.edge_invalid(xd, dd): return True
        if self.edge_invalid(dd, v): return True

        return False

calls = 0

def backtracking_search(assignment, instance):
    global calls
    calls += 1
    print assignment.variables
    # jeśli mamy rozwiązanie lub takowego nie ma - kończymy
    if assignment.is_complete() and not instance.is_violating_constraints(*assignment.variables):
        return assignment

    # pobierz zmienną bez wartości
    var = assignment.get_unassigned_variable()

    # dla wszystkich wartości z domeny zmiennej
    for val in var.domain:
        # przypisz tą wartość
        var.value = val
        # i sprawdź czy przypisanie spowodowało naruszenie więzów.
        if instance.is_violating_constraints(*assignment.variables):
            # jeśli tak cofnij przypisanie i spróbuj z następną wartością
            var.value = None
            continue
        # przypisanie było poprawne, powtórz dka kolejnej zmiennej (zejscie w dół drzewa)
        result = backtracking_search(assignment, instance)
        # mamy wynik, wróć w górę
        if result is not None:
            return result
        # niżej nie udało się spełnić ograniczeń, wyzeruj podstawienie
        else:
            var.value = None

    # nawrót
    return None


if __name__ == "__main__":
    magic = MagicSquare()
    initial = magic.get_initial_assignment()
    res = backtracking_search(initial, magic)
    if res is None:
        print "Nope, nie da się."
    else:
        print res.variables
print calls
