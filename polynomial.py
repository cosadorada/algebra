# aim here is to make a polynomial class

class Polynomial:
    def __init__(self, terms: dict, field=None):
        self.terms = {
            power:coeff  for power, coeff in terms.items() if coeff != 0
        }
        # a dictionary, keys are powers, values are non-zero coefficients

        #degree doesn't make sense with multivariate polys
        self.degree = max(self.terms.keys()) if self.terms else -1
        

    def __add__(self, other):
        result = self.terms.copy()
        for power, coeff in other.terms.items():
            if power in result:
                result[power] += coeff
            else:
                result[power] = coeff
        return Polynomial(result)

    def __sub__(self, other):
        result = self.terms.copy()
        for power, coeff in other.terms.items():
            if power in result:
                result[power] -= coeff
            else:
                result[power] = -coeff
        return Polynomial(result)

    def __mul__(self, other):
        result = {}
        for power1, coeff1 in self.terms.items():
            for power2, coeff2 in other.terms.items():
                result_power = power1 * power2 # multiply for monomials
                result_coeff = coeff1 * coeff2
                if result_power in result:
                    result[result_power] += result_coeff
                else:
                    result[result_power] = result_coeff
        return Polynomial(result)


    def leading_coefficient(self):
        if not self.terms:
            return 0
        return self.terms[self.leading_monomial()]

    def leading_monomial(self):
        if not self.terms:
            return None
        return max(self.terms)

    def leading_term(self):
        if not self.terms:
            return None
        return Polynomial({self.leading_monomial(): self.leading_coefficient()})


    def division_by(self, other):
        if not other.terms:
            raise ValueError("Cannot divide by zero polynomial")
        q = Polynomial({})
        r = Polynomial({})
        p = Polynomial(self.terms.copy())
        while p.terms:
            if other.leading_monomial().divides(p.leading_monomial()):

                t = other.leading_monomial().quotient(p.leading_monomial())

                q = q + Polynomial({t: p.leading_coefficient() / other.leading_coefficient()})
                p = p - (Polynomial({t: p.leading_coefficient() / other.leading_coefficient()}) * other)
            else:
                r = r + Polynomial({p.leading_monomial(): p.leading_coefficient()})
                p = p - Polynomial({p.leading_monomial(): p.leading_coefficient()})
        return q, r

    def divide_by_list(self, divisors: list):
        if not divisors:
            raise ValueError('Divisors list must be non-empty')
        quotients = [Polynomial({}) for _ in divisors]
        remainder = Polynomial({})
        p = Polynomial(self.terms.copy())
        while p.terms:
            divided = False
            for i, divisor in enumerate(divisors):
                if divisor.leading_monomial().divides(p.leading_monomial()):
                    t = divisor.leading_monomial().quotient(p.leading_monomial())
                    quotients[i] = quotients[i] + Polynomial({t: p.leading_coefficient() / divisor.leading_coefficient()})
                    p = p - (Polynomial({t: p.leading_coefficient() / divisor.leading_coefficient()}) * divisor)
                    divided = True
                    break # out of for loop to restart with new remainder
            if not divided:
                leading_term = p.leading_term()
                remainder = remainder + leading_term
                p = p - leading_term
        
        return quotients, remainder



    # The below now don't work for multivariate polynomials.
    def evaluate(self, x):
        value = 0
        for power, coeff in self.terms.items():
            value += coeff * (x ** power)
        return value

    def derivative(self):
        result = {}
        for power, coeff in self.terms.items():
            if power > 0:
                result[power - 1] = coeff * power
        return Polynomial(result)

    def __str__(self):
        string = ""
        for power, coeff in sorted(self.terms.items(), reverse=True):
            if coeff == 0:
                continue
            if power > 1:
                string += f"{coeff}x^{power} + "
            elif power == 1:
                string += f"{coeff}x + "
            else: 
                string += f"{coeff} "
        return string



class Monomial:
# For multiple variables, represent as a product. Ignores coefficients.
    def __init__(self, powers):
        self.powers = tuple(powers)
        if any(p < 0 for p in self.powers):
            raise ValueError("Powers must be non-negative integers")

    def __mul__(self, other):
        if len(self.powers) != len(other.powers):
            raise ValueError("Different number of variables")
        return Monomial(a + b for a, b in zip(self.powers, other.powers))

    def divides(self, other):
        if len(self.powers) != len(other.powers):
            raise ValueError("Different number of variables")
        return all(a <= b for a, b in zip(self.powers, other.powers))

    def quotient(self, other):
        # This returns other / self, so long as self divides other. 
        if not self.divides(other):
            raise ValueError("Monomial does not divide the other")
        return Monomial(b - a for a, b in zip(self.powers, other.powers))

    def lcm(self, other):
        if len(self.powers) != len(other.powers):
            raise ValueError("Different number of variables")
        return Monomial(max(a, b) for a, b in zip(self.powers, other.powers))
    

    def __str__(self):
        return " * ".join(f"x{i+1}^{power}" for i, power in enumerate(self.powers) if power != 0)
    def __repr__(self):
        return str(self)


    def __eq__(self, other):
        return self.powers == other.powers
    def __hash__(self):
        return hash(self.powers)

    #comparison operators are done well by tuples. - lexicographic order.
    def __lt__(self, other):
        return self.powers < other.powers
    def __gt__(self, other):
        return self.powers > other.powers



if __name__ == "__main__":
    '''    p1 = Polynomial({4:2, 3:0, 2:1, 0:7})
    print(p1)  # should print "2x^4 + 1x^2 + 7 "
    p2 = Polynomial({3:-3, 1:5, 0:-7})
    print(p2) # should print "-3x^3 + 5x + -7 "
    print(p1+p2)
    print(p1-p2)
    print(p1*p2) # "-6x^7 + 7x^5 + -14x^4 + -16x^3 + -7x^2 + 35x + -49 "
    print(p1.degree, p2.degree, (p1*p2).degree) 
    print(p1.leading_coefficient(), p2.leading_coefficient(), (p1*p2).leading_coefficient())
    print(p1.evaluate(0), p1.evaluate(1))
    print(p1.derivative()) # should print "8x^3 + 2x + "
    '''
    m1 = Monomial((2, 1, 0)) #x2y
    m2 = Monomial((1, 2, 0)) #xy2
    print(m1 * m2) # should print "x1^3 * x2^3"
    print(m1.divides(m2)) # should print False

    poly1 = Polynomial({Monomial((2, 1)): 3, Monomial((0, 1)): 5}) # 3x^2 * y + 5y
    poly2 = Polynomial({Monomial((1, 2)): 4, Monomial((0, 1)): -2}) # 4x * y^2 - 2y
    polym1 = poly1.leading_monomial()
    polym2 = poly2.leading_monomial()
    print(polym1, 'and', polym2) 
    lcm = polym1.lcm(polym2)
    print("LCM of leading monomials:", lcm) # should print "x1^2 * x2^2"
