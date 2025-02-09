from flask import Flask, render_template, request, make_response, jsonify
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import io, base64
from sympy import symbols, lambdify, sympify
import re
from func import create_function, bisection, newton, plot_convergence

matplotlib.use('Agg')  

app = Flask(__name__)

@app.route("/", methods = ['GET','POST'])
def index():

    bisection_iters, bisection_errors, newton_iters, newton_errors = [], [], [], []
    graph = None
    result = None

    if request.method == 'POST':

        data = request.json
        
        f = data['fun']
        df = data['df']
        a = float(data['a'])
        b = float(data['b'])

        f = create_function(f)
        df = create_function(df)

        bisection_iters, bisection_errors = bisection(f, a, b)     
        result, newton_iters, newton_errors = newton(f, df, (a+b)/2)
        graph = plot_convergence(bisection_iters, bisection_errors, newton_iters, newton_errors)
        return jsonify({"graph": graph, "result": result})

    
    return render_template('index.html', result = result, graph = graph)

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)