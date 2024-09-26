from py_ecc.fields import bn128_FQ as FQ
from py_ecc import bn128
from functools import reduce

from zkp.groth16.code_to_r1cs import code_to_r1cs_with_inputs

from zkp.groth16.qap_creator_lcm import (
    r1cs_to_qap_times_lcm, 
    create_solution_polynomials, 
    create_divisor_polynomial,
    add_polys,
    subtract_polys,
    multiply_polys
)

from zkp.groth16.poly_utils import (
    # _multiply_polys,
    _add_polys,
    # _subtract_polys,
    # _div_polys,
    # _eval_poly,
    # _multiply_vec_matrix,
    _multiply_vec_vec,
    getNumWires,
    getNumGates,
    getFRPoly1D,
    getFRPoly2D,
    ax_val,
    bx_val,
    cx_val,
    zx_val,
    hxr,
    hx_val
)

from zkp.groth16.setup import (
    sigma11,
    sigma12,
    sigma13,
    sigma14,
    sigma15,
    sigma21,
    sigma22
)

from zkp.groth16.proving import (
    proof_a,
    proof_b,
    proof_c
)

from zkp.groth16.verifying import verify

g1 = bn128.G1
g2 = bn128.G2

mult = bn128.multiply
pairing = bn128.pairing
add = bn128.add
neg = bn128.neg

class FR(FQ):
    field_modulus = bn128.curve_order

def test_code_to_r1cs():
#     code = """
# def qeval(x, z, w):
#     y = x**3 + z*w
#     return y + x + 5
# """
#    inputs = [3,4,5]
    code = """
def qeval(x):
    y = x**3
    return y + x + 5
"""
    inputs = [3]

    r, A, B, C  = code_to_r1cs_with_inputs(code, inputs)

    # print('r')
    # print(r)
    # print('A')
    # for x in A: print(x)
    # print('B')
    # for x in B: print(x)
    # print('C')
    # for x in C: print(x)

    return r, A, B, C

def test_r1cs_qap_lcm():
    r, A, B, C = test_code_to_r1cs()

    Ap, Bp, Cp, Z = r1cs_to_qap_times_lcm(A, B, C)

    # print('Ap')
    # for x in Ap: print(x)
    # print('Bp')
    # for x in Bp: print(x)
    # print('Cp')
    # for x in Cp: print(x)
    
    # print('Z')
    # print(Z)
    
    #Apoly = Ap.r
    #Bpoly = Bp.r
    #Cpoly = Cp.r
    Apoly, Bpoly, Cpoly, sol = create_solution_polynomials(r, Ap, Bp, Cp)
    
    # print('Apoly(A(x))')
    # print(Apoly)
    
    # print('Bpoly(B(x))')
    # print(Bpoly)
    
    # print('Cpoly(C(x))')
    # print(Cpoly)
    
    # print('Sol(A(x)*B(x)-C(x))')
    # print(sol)
    
    # print('Z cofactor, H')
    H = create_divisor_polynomial(sol, Z)
    # A(x)*B(x)-C(x) = H*Z
    # <==>
    # (A(x)*B(x)-C(x)) / Z = H
    # <==>
    # (A(x)*B(x)-C(x)) / (x-1)(x-2)(x-3)..(x-k) = H
    # print(H)
    # hz = multiply_polys(H, Z)

    # hz_int = [round(val) for val in hz]
    # sol_int = [round(val) for val in sol]
    # # print("hz(int) : {}".format(hz_int))
    # # # print("type(hz_int[0]) : {}".format(type(hz_int[0])))
    # # print("sol(int) : {}".format(sol_int))
    # # print("type(sol_int[0]) : {}".format(type(sol_int[0])))

    # print("hz_int == sol_int ? {}".format(hz_int == sol_int))
    

    # test1 = (hz_int == sol_int)
    
    # # print("multiply_polys(H, Z) {}".format(multiply_polys(H, Z)))
    # # print("sol : {}".format(sol))

    # print("Test : r1cs_to_qap_lcm : {}".format(test1))

    return Ap, Bp, Cp, Z, r


def test_setup():
    # EXAMPLE TOXIC
    alpha = FR(3926)
    beta = FR(3604)
    gamma = FR(2971)
    delta = FR(1357)
    x_val = FR(3721)

    # EXAMPLE POLYNOMIAL
    # Ap = [
    #     [-60.0, 110.0, -60.0, 10.0],
    #     [96.0, -136.0, 60.0, -8.0],
    #     [0.0, 0.0, 0.0, 0.0],
    #     [-72.0, 114.0, -48.0, 6.0],
    #     [48.0, -84.0, 42.0, -6.0],
    #     [-12.0, 22.0, -12.0, 2.0]
    # ]
    # Bp = [
    #     [36.0, -62.0, 30.0, -4.0],
    #     [-24.0, 62.0, -30.0, 4.0],
    #     [0.0, 0.0, 0.0, 0.0],
    #     [0.0, 0.0, 0.0, 0.0],
    #     [0.0, 0.0, 0.0, 0.0],
    #     [0.0, 0.0, 0.0, 0.0]
    # ]
    # Cp = [
    #     [0.0, 0.0, 0.0, 0.0],
    #     [0.0, 0.0, 0.0, 0.0],
    #     [-144.0, 264.0, -144.0, 24.0],
    #     [576.0, -624.0, 216.0, -24.0],
    #     [-864.0, 1368.0, -576.0, 72.0],
    #     [576.0, -1008.0, 504.0, -72.0]
    # ]
    # Z = [3456.0, -7200.0, 5040.0, -1440.0, 144.0]
    # R = [1, 3, 35, 9, 27, 30]

    Ap, Bp, Cp, Z, R = test_r1cs_qap_lcm()

    # print("Ap : {}".format(Ap))
    # print("Bp : {}".format(Bp))
    # print("Cp : {}".format(Cp))
    # print("Z : {}".format(Z))
    # print("R : {}".format(R))
    # print("")

    Ax = getFRPoly2D(Ap)
    Bx = getFRPoly2D(Bp)
    Cx = getFRPoly2D(Cp)
    Zx = getFRPoly1D(Z)
    Rx = getFRPoly1D(R)
    # print("Ax : {}".format(Ax))
    # print("Bx : {}".format(Bx))
    # print("Cx : {}".format(Cx))
    # print("Zx : {}".format(Zx))
    # print("Rx : {}".format(Rx))
    # print("")

    # (Ax.R * Bx.R - Cx.R) / Zx = Hx .... r
    Hx, r = hxr(Ax, Bx, Cx, Zx, R)
    # print("H(x) : {}".format(Hx))
    # print("r : {}".format(r))

    Hx_val = hx_val(Hx, x_val)

    numGates = getNumGates(Ax)
    numWires = getNumWires(Ax)
    
    Ax_val = ax_val(Ax, x_val)
    Bx_val = bx_val(Bx, x_val)
    Cx_val = cx_val(Cx, x_val)
    Zx_val = zx_val(Zx, x_val)

    s11 = sigma11(alpha, beta, delta)
    s12 = sigma12(numGates, x_val)
    s13, VAL = sigma13(numWires, alpha, beta, gamma, Ax_val, Bx_val, Cx_val)
    s14 = sigma14(numWires, alpha, beta, delta, Ax_val, Bx_val, Cx_val)
    s15 = sigma15(numGates, delta, x_val, Zx_val)
    s21 = sigma21(beta, delta, gamma)
    s22 = sigma22(numGates, x_val)

    #TEST1 : r should be zero
    t1 = (reduce((lambda x, y : x*y), r) == 0)
    # print("r : {}".format(r))

    lhs = _multiply_vec_vec(Rx, Ax_val) * _multiply_vec_vec(Rx, Bx_val) - _multiply_vec_vec(Rx, Cx_val)
    rhs = Zx_val * Hx_val

    #TEST2 : lhs == rhs
    t2 = (lhs == rhs)

    print("TEST1 {}".format(t1))
    print("TEST2 {}".format(t2))
    
    sigmas = [s11, s12, s13, s14, s15, s21, s22]
    sol_polys = [Ax_val, Bx_val, Cx_val, Hx_val, Zx_val]
    polys = [Ax, Bx, Cx, Hx, Zx, Rx]

    o = {"sigmas" : sigmas, "sol_polys" : sol_polys, "VAL" : VAL, "numGatesWires":[numGates, numWires], "polys" : polys} 

    return o

def test_proving_and_verifying():

    # EXAMPLE TOXIC
    alpha = FR(3926)
    beta = FR(3604)
    gamma = FR(2971)
    delta = FR(1357)
    x_val = FR(3721)

    out = test_setup()
    
    sigmas = out["sigmas"]
    sol_polys = out["sol_polys"]
    polys = out["polys"]
    
    VAL = out["VAL"]

    numWires = out["numGatesWires"][1]
    numGates = out["numGatesWires"][0]

    Ax = polys[0]
    Bx = polys[1]
    Cx = polys[2]
    Hx = polys[3]
    Zx = polys[4]
    Rx = polys[5]

    Ax_val = sol_polys[0]
    Bx_val = sol_polys[1]
    Cx_val = sol_polys[2]
    Hx_val = sol_polys[3]
    Zx_val = sol_polys[4]

    sigma1_1 = sigmas[0]
    sigma1_2 = sigmas[1]
    sigma1_3 = sigmas[2]
    sigma1_4 = sigmas[3]
    sigma1_5 = sigmas[4]
    sigma2_1 = sigmas[5]
    sigma2_2 = sigmas[6]

    # EXAMPLE r, s
    r = FR(4106)
    s = FR(4565)

    proof_A = proof_a(sigma1_1, sigma1_2, Ax, Rx, r)
    proof_B = proof_b(sigma2_1, sigma2_2, Bx, Rx, s)
    proof_C = proof_c(sigma1_1, sigma1_2, sigma1_4, sigma1_5, Bx, Rx, Hx, s, r, proof_A)

    def scalar_vec(scalar, vec):
        return [scalar*num for num in vec]
    
    ### PROOF COMPLETENESS CHECK ###

    A = alpha + _multiply_vec_vec(Rx, Ax_val) + r*delta
    B = beta + _multiply_vec_vec(Rx, Bx_val) + s*delta

    C0 = 1/delta 
    C1 = Rx[1:numWires-1] #vec
    C1_1 = scalar_vec(beta, Ax_val[1:numWires-1])
    C1_2 = scalar_vec(alpha, Bx_val[1:numWires-1])
    C1_3 = Cx_val[1:numWires-1]
    C2 = Hx_val*Zx_val
    C3 = A*s + B*r - r*s*delta

    C1112 = _add_polys(C1_1, C1_2) # vec
    C111213 = _add_polys(C1112, C1_3) # vec
    C1111213 = _multiply_vec_vec(C1, C111213) #num

    C = C0 * (C1111213 + C2) + C3

    lhs = A*B 

    rpub = [Rx[0], Rx[-1]]
    valpub = [VAL[0], VAL[-1]]

    rhs = alpha*beta + gamma*_multiply_vec_vec(rpub,valpub) + C*delta

    print("#PROOF COMPLETENESS CHECK#")
    print("rhs : {}".format(rhs))
    print("lhs : {}".format(lhs))
    print("rhs == lhs ? : {}".format(rhs == lhs))
    print("proof A check : {}".format(proof_A == mult(g1, int(A))))
    print("proof B check : {}".format(proof_B == mult(g2, int(B))))
    print("proof C check : {}".format(proof_C == mult(g1, int(C))))

    ##verifying##

    very_result = verify(numWires, proof_A, proof_B, proof_C, sigma1_1, sigma1_3, sigma2_1, Rx)

    print("Verifying ? : {}".format(very_result))

    return proof_A, proof_B, proof_C

if __name__ == "__main__":
    #test_code_to_r1cs()
    #test_r1cs_qap_lcm()
    # test_setup()
    test_proving_and_verifying()
