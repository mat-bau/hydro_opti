"""
Hydroelectric dam optimal management — LINMA1702 Part 1
Linear programming model solved with CVXPY + HiGHS.
"""

import numpy as np
import cvxpy as cp


# ─── tunable globals (easy to override for sensitivity analysis) ──────────────
DEFAULT_SOLVER = cp.HIGHS
DELTA_T = 1.0  # hours — discretisation step


# ─── data parsing ─────────────────────────────────────────────────────────────

def parse_scenario(filepath: str) -> dict:
    """
    Parse a scenario .txt file into a parameter dictionary.

    File format: alternating keyword / value blocks separated by blank lines.
    Scalar parameters are stored as floats, vector parameters (F, P) as
    1-D numpy arrays of length N.
    """
    with open(filepath, "r") as fh:
        content = fh.read()

    tokens = content.split()
    params = {}
    i = 0
    current_key = None
    vector_buffer = []

    SCALAR_KEYS = {"N", "V0", "Vmin", "Vmax", "Tmax", "Dmax", "Mmax",
                   "ET", "ME", "TDmin", "VTmax", "VDmax"}
    VECTOR_KEYS = {"F", "P"}

    while i < len(tokens):
        token = tokens[i]

        if token in SCALAR_KEYS:
            # flush any pending vector
            if current_key in VECTOR_KEYS and vector_buffer:
                params[current_key] = np.array(vector_buffer, dtype=float)
                vector_buffer = []

            current_key = token
            params[current_key] = float(tokens[i + 1])
            i += 2

        elif token in VECTOR_KEYS:
            # flush any pending vector
            if current_key in VECTOR_KEYS and vector_buffer:
                params[current_key] = np.array(vector_buffer, dtype=float)
                vector_buffer = []

            current_key = token
            i += 1

        else:
            # accumulate numeric values for the current vector key
            if current_key in VECTOR_KEYS:
                vector_buffer.append(float(token))
            i += 1

    # flush last vector
    if current_key in VECTOR_KEYS and vector_buffer:
        params[current_key] = np.array(vector_buffer, dtype=float)

    params["N"] = int(params["N"])
    return params


# ─── optimisation model ───────────────────────────────────────────────────────

def _build_variables(N: int):
    """Declare all CVXPY decision variables."""
    T = cp.Variable(N, name="T", nonneg=True)   # turbined flow   [m³/h]
    D = cp.Variable(N, name="D", nonneg=True)   # spillage flow   [m³/h]
    M = cp.Variable(N, name="M", nonneg=True)   # pumped flow     [m³/h]
    V = cp.Variable(N + 1, name="V", nonneg=True)  # reservoir vol  [m³]
    return T, D, M, V


def _build_constraints(T, D, M, V, params: dict) -> list:
    """
    Assemble all linear constraints.

    Discretisation convention:
      - T[k], D[k], M[k] are the constant flows during hour k (k = 0..N-1).
      - V[0] = V_initial, V[k+1] = V[k] + (F[k] + M[k] - T[k] - D[k]) * Δt
      - Rate-of-change constraints use finite differences:
            |T[k] - T[k-1]| ≤ VTmax * Δt  for k = 1..N-1
    """
    N   = params["N"]
    F   = params["F"]
    V0  = params["V0"]
    Vmin = params["Vmin"]
    Vmax = params["Vmax"]
    Tmax = params["Tmax"]
    Dmax = params["Dmax"]
    Mmax = params["Mmax"]
    TDmin = params["TDmin"]
    VTmax = params["VTmax"]
    VDmax = params["VDmax"]
    dt   = DELTA_T

    constraints = []

    # --- initial and terminal volume conditions
    constraints += [V[0] == V0, V[N] == V0]

    # --- reservoir dynamics (water balance per time step)
    for k in range(N):
        constraints.append(
            V[k + 1] == V[k] + (F[k] + M[k] - T[k] - D[k]) * dt
        )

    # --- volume bounds
    constraints += [V >= Vmin, V <= Vmax]

    # --- flow upper bounds
    constraints += [T <= Tmax, D <= Dmax, M <= Mmax]

    # --- minimum total outflow (security / ecological constraint)
    constraints += [T + D >= TDmin]

    # --- rate-of-change constraints (finite-difference approximation of |x'| ≤ bound)
    for k in range(1, N):
        constraints += [
            T[k] - T[k - 1] <=  VTmax * dt,
            T[k - 1] - T[k] <=  VTmax * dt,
            D[k] - D[k - 1] <=  VDmax * dt,
            D[k - 1] - D[k] <=  VDmax * dt,
        ]

    return constraints


def _build_objective(T, D, M, params: dict) -> cp.Expression:
    """
    Revenue = sum_k P[k] * (ET * T[k] - ME * M[k]) * Δt

    Units: [€/MWh] * [MWh/m³] * [m³/h] * [h] = [€]
    """
    P  = params["P"]
    ET = params["ET"]
    ME = params["ME"]
    dt = DELTA_T

    revenue = cp.sum(cp.multiply(P, ET * T - ME * M)) * dt
    return revenue


# ─── public entry point ───────────────────────────────────────────────────────

def hydro(data: str) -> dict:
    """
    Solve the hydroelectric dam optimisation problem.

    Parameters
    ----------
    data : str
        Path to a scenario file (e.g. "BelgiumScenario1.txt").

    Returns
    -------
    sol : dict with keys
        V       – reservoir volumes [m³], shape (N+1,)
        T       – turbined flows    [m³/h], shape (N,)
        D       – spillage flows    [m³/h], shape (N,)
        M       – pumped flows      [m³/h], shape (N,)
        valopt  – optimal objective value [€]
        problem – the solved cp.Problem (for dual values, status, etc.)
        params  – parsed parameter dictionary
    """
    params = parse_scenario(data)
    N = params["N"]

    T, D, M, V = _build_variables(N)
    constraints = _build_constraints(T, D, M, V, params)
    objective   = _build_objective(T, D, M, params)

    problem = cp.Problem(cp.Maximize(objective), constraints)
    problem.solve(solver=DEFAULT_SOLVER, verbose=False)

    if problem.status not in (cp.OPTIMAL, cp.OPTIMAL_INACCURATE):
        raise RuntimeError(f"Solver ended with status: {problem.status}")

    sol = {
        "V":      V.value,
        "T":      T.value,
        "D":      D.value,
        "M":      M.value,
        "valopt": problem.value,
        "problem": problem,
        "params":  params,
    }
    return sol


# ─── reference strategy (Q1.5) ────────────────────────────────────────────────

def reference_strategy_revenue(params: dict) -> float:
    """
    Revenue of the no-pumping reference strategy:
    T[k] = F[k] at every step (turbine compensates inflow exactly),
    D[k] = 0, M[k] = 0.

    This ignores volume and ramp constraints, giving an upper bound on what
    such a strategy can achieve; a feasibility check is left to the caller.
    """
    P  = params["P"]
    F  = params["F"]
    ET = params["ET"]
    dt = DELTA_T
    return float(np.sum(P * ET * F) * dt)


def no_pump_revenue(sol: dict) -> float:
    """Revenue from the optimal solution with pumping disabled (re-solve)."""
    params_no_pump = dict(sol["params"])
    params_no_pump["Mmax"] = 0.0

    N = params_no_pump["N"]
    T, D, M, V = _build_variables(N)
    constraints = _build_constraints(T, D, M, V, params_no_pump)
    objective   = _build_objective(T, D, M, params_no_pump)

    prob = cp.Problem(cp.Maximize(objective), constraints)
    prob.solve(solver=DEFAULT_SOLVER, verbose=False)
    return prob.value