from flask import Flask, render_template, request, make_response, jsonify
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import io, base64
from sympy import symbols, lambdify, sympify
import re

def create_function(expr_str):
    x = symbols("x")
    try:
        # Fix implicit multiplication: convert "2x" -> "2*x", "3x^2" -> "3*x**2"
        expr_str = re.sub(r'(?<![\*\+\-\/\(\^])x', r'*x', expr_str)
        
        # Ensure first character is not '*'
        if expr_str.startswith('*'):
            expr_str = expr_str[1:]

        # Convert string expression into a SymPy expression safely
        expr = sympify(expr_str)
        
        # Convert symbolic expression to a function
        return lambdify(x, expr)
    except Exception as e:
        raise ValueError(f"Invalid function expression: {expr_str}. Error: {e}")


def bisection(f, a, b, tol=1e-6, max_iter=100):
    errors, iterations = [], []

    if f(a) * f(b) >= 0:
        return [], []
    for i in range(max_iter):
        c = (a + b) / 2
        error = abs(f(c))
        errors.append(error)
        iterations.append(i)
        if error < tol:
            break
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
    return iterations, errors

def newton(f, df, x0, tol=1e-6, max_iter=100):
    errors, iterations = [], []
    x = x0
    for i in range(max_iter):
        if df(x) == 0:
            break
        x_new = x - f(x) / df(x)
        error = abs(x_new - x)
        errors.append(error)
        iterations.append(i)
        if error < tol:
            break
        x = x_new
    return x ,iterations, errors

def plot_convergence(bisection_iters, bisection_errors, newton_iters, newton_errors):
    plt.figure(figsize=(8, 6))
    if bisection_iters:
        plt.plot(bisection_iters, bisection_errors, label='Bisection', marker='o')
    if newton_iters:
        plt.plot(newton_iters, newton_errors, label='Newton', marker='^')
    plt.xlabel('Iteration')
    plt.ylabel('Error')
    plt.title('Convergence of Root-Finding Algorithms')
    plt.legend()
    plt.grid()
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    plt.close()

    return base64.b64encode(img.getvalue()).decode()