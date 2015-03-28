# coding=utf-8
class DomainException(Exception):
    pass

class Variable(object):
    def __init__(self, fixed_value=None):
        # załpżono, że dziedzina dla wszystkich zmiennych jest taka sama [1..20]
        # ale równie dobrze może być przekazywana do konstruktora
        self.domain =  range(1,21) if fixed_value is None else [fixed_value]
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

    # mały helper aby łątwiej tworzyć listę zmiennych z podanych wartości
    # więcej na temat tej składni można znaleźć pod hasłem list comprehension
    def get_variables_from_values(self, values):
        return [Variable(x) for x in values]

    # początkowe wartości zmiennych. Liczby oznaczają stałą wartość, None to miejsca
    # do których ma wstawić algorytm
    def get_initial_assignment(self):
        return Assingment(self.get_variables_from_values([None, None, None, None,
                                                          5, None, None, 8,
                                                          9, None, 7, None,
                                                          None, None, 14, None
                                                          ]))

    # sprawdza czy wiersz o indeksie row spełnia ograniczenia
    def row_satisfies_constraint(self, row, full_state, desired_sum):
        """

        :param row: wiersz do sprawdzenia
        :param full_state: zmienne
        :param desired_sum: oczekiwana suma
        :return: True jeśli spełnia, False jeśli łamie
        """
        # wyciągnięcie pojedynczego wiersza z całości listy zmiennych
        sliced_row = full_state[row * self.square_size:row * self.square_size+self.square_size]
        # jeśli któraś zmienna jest nieprzypisana to wiersz nie łamie ograniczeń
        has_none = bool([x for x in sliced_row if x.value == None])
        if has_none:
            return True
        # jeśli wszystkie mają wartość to spradzamy czy ich suma jest taka jak oczekiwano
        return sum(sliced_row) == desired_sum

    # analogicznie jak row_satisfies_constraint tylko, że dla kolumn
    def col_satisfies_constraint(self, col, full_state, desired_sum):
        sliced_row = full_state[col::self.square_size]
        has_none = bool([x for x in sliced_row if x.value == None])
        if has_none:
            return True
        return sum(sliced_row) == desired_sum

    # sprawdza czy podstawienie narusza ograniczenia
    def is_violating_constraints(self, assigment):
        #alias coby mniej pisać ;)
        v = assigment.variables

        # spawdzenie wierszy
        for row_index in range(0,self.square_size):
            if not self.row_satisfies_constraint(row_index, v, self.summary):
                return True

        # kolumn
        for col_index in range(0,self.square_size):
            if not self.col_satisfies_constraint(col_index, v, self.summary):
                return True

        # przekątnych
        # tutaj oczywiście można zrobić to tego funkcje jak poprzednio ale już sobie odpuściłem

        if not assmagic_square.pyigment.is_complete():
            return False

        if v[0].value + v[5].value + v[10].value + v[15].value != self.summary:
            return True

        if v[3].value + v[6].value + v[9].value + v[12].value != self.summary:
            return True

        # sprawdziliśmy wszystkie warunki - dane przypisanie jest OK
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
    magic = MagicSquare()
    initial = magic.get_initial_assignment()
    res = backtracking_search(initial, magic)
    if res is None:
        print "Nope, nie da się."
    else:
        res.pretty_print()

