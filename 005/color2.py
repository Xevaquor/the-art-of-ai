# coding=utf-8
class DomainException(Exception):
    pass


class Colour(object):
    def __init__(self):
        pass

    Red, Green, Blue = range(3)


class Variable(object):
    def __init__(self, fixed_value=None):
        # załpżono, że dziedzina dla wszystkich zmiennych jest taka sama [1..20]
        # ale równie dobrze może być przekazywana do konstruktora
        self.domain = [Colour.Red, Colour.Green, Colour.Blue] if fixed_value is None else [fixed_value]
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


class Australia(object):
    def __init__(self):
        self.constraints = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (2, 4), (2, 5), (3, 4), (4, 5)]

    # mały helper aby łątwiej tworzyć listę zmiennych z podanych wartości
    # więcej na temat tej składni można znaleźć pod hasłem list comprehension
    def get_variables_from_values(self, values):
        return [Variable(x) for x in values]

    # początkowe wartości zmiennych. Liczby oznaczają stałą wartość, None to miejsca
    # do których ma wstawić algorytm
    def get_initial_assignment(self):
        return Assingment(self.get_variables_from_values([None] * 7))

    def edge_invalid(self, a, b):
        if not a.is_assigned or not b.is_assigned:
            return False

        return a.value == b.value


    # sprawdza czy podstawienie narusza ograniczenia
    def is_violating_constraints(self, assignment):
        # alias co by mniej pisać ;)
        v = assignment.variables

        for a, b in self.constraints:
            if self.edge_invalid(v[a],v[b]):
                return True

        return False

def backtracking_search(assignment, instance):
    # jeśli mamy rozwiązanie lub takowego nie ma - kończymy
    if assignment.is_complete() and not instance.is_violating_constraints(assignment):
        return assignment

    # pobierz zmienną bez wartości
    var = assignment.get_unassigned_variable()

    # dla wszystkich wartości z domeny zmiennej
    for val in var.domain:
        # przypisz tą wartość
        var.value = val
        # i sprawdź czy przypisanie spowodowało naruszenie więzów.
        if instance.is_violating_constraints(assignment):
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
    a = Australia()
    initial = a.get_initial_assignment()
    res = backtracking_search(initial, a)
    if res is None:
        print "Nope, nie da się."
    else:
        print res.variables
