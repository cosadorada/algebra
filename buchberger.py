from polynomial import Polynomial
from polynomial import Monomial




def s_polynomial(f, g):
    #Get the S-polynomial of f and g

    f_lm = f.leading_monomial()
    g_lm = g.leading_monomial()
    lcm_monomial = f_lm.lcm(g_lm)

    f_monomial = f_lm.quotient(lcm_monomial)
    g_monomial = g_lm.quotient(lcm_monomial)

    f_multiplier = Polynomial({f_monomial: 1/f.leading_coefficient()})
    g_multiplier = Polynomial({g_monomial: 1/g.leading_coefficient()})

    s_polynomial = (f_multiplier * f) - (g_multiplier * g)

    return s_polynomial

def buchberger_algorithm(polynomials):
    #implement Buchberger's algorithm to compute Gröbner basis

    G = list(polynomials)

    pairs = [(f, g) for i, f in enumerate(G) for g in G[i+1:]]
    while pairs:
        f, g = pairs.pop(0)
        s_poly = s_polynomial(f, g)

        _, remainder = s_poly.divide_by_list(G)
        if remainder.terms:
            G.append(remainder)
            pairs.extend([(remainder, h) for h in G[:-1]])

    return G


f1 = Polynomial({
    Monomial((2, 0)): 1,
    Monomial((0, 1)): -1
})

f2 = Polynomial({
    Monomial((1, 1)): 1,
    Monomial((0, 0)): -1
})

G = buchberger_algorithm([f1, f2])

for f in G:
    print(f.terms)

