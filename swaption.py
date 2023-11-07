import numpy as np

def NPV_swap(floating_rate, fixed_rate, N, pay_rate, maturity) -> float:
    """
    Calculates the NPV of the underlying interest rate swap
    """
    fixed_leg, floating_leg = list(), list()
    spread = 0.01

    remaining_maturity = len(floating_rate)

    # Walk through time, start at t=1
    for i in range(remaining_maturity):
        floating_leg.append(floating_rate[i] * N / (((1 + fixed_rate) ** i)))
        fixed_leg.append((fixed_rate + spread) * N / ((1 + fixed_rate) ** i))

    pv_floating = sum(floating_leg)
    pv_fixed = sum(fixed_leg)

    return pv_fixed - pv_floating


def swaption(floating_rate, fixed_rate, N, pay_rate, maturity, strike) -> float:
    """
    Calculates the returns of a swaption if it is exercised.
    """
    return max(0, NPV_swap(floating_rate, fixed_rate, N, pay_rate, maturity) - N * strike)

def bermudan_swaption(floating_rate, fixed_rate, N, pay_rate, maturity, strike) -> float:
    """
    Calculates the payoff for an Bermudan Swaption. Checks from t=1 whether the swaption
    is exercised.
    """
    for t in range(maturity):

        # Calculate the current NPV of the swaption
        swap_value = swaption(floating_rate[t:], fixed_rate, N, pay_rate, maturity, strike)

        # NPV > 0 implies that the swaption is exercised
        if swap_value > 0:
            print(f'Present Value: {swap_value}')
            print(f'Time {t}')
            return swap_value

    return 0

if __name__ == "__main__":
    floating_rate = [0.1, 0.1, 0.11, 0.001, 0.01] # To be modeled interest rate
    fixed_rate = 0.03 # Random fixed rate
    N = 1 # Notional value
    maturity = len(floating_rate)
    pay_rate = 1 # Simplicity of payments, works only if at least one payment per year
    strike = 0.04 # Strike rate

    bermudan_swaption(floating_rate, fixed_rate, N, pay_rate, maturity, strike)
