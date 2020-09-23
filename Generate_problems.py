# @Author: Henrik Pinholt <henrikpinholt>
# @Date:   23-Sep-2020
# @Email:  henrikpinholt@hotmail.com
# @Last modified by:   henrikpinholt
# @Last modified time: 23-Sep-2020
import pandas as pd
import numpy as np
from pdflatex import PDFLaTeX

# Set the parameters for the table
nrows, ncolumns = 6, 4
max_number1, max_number2 = 1000, 100
real_nrows, real_ncolumns = nrows * 2, ncolumns * 2
pdf_name = "Math_problems"

# Generate table in python
table, solution_table = [], []
for row_n in range(real_nrows):
    row_insert = []
    sol_row_insert = []
    for column_n in range(0, real_ncolumns, 2):
        # Check if division or multiplication (are we halfway?)
        number1, number2 = (
            np.random.randint(2, max_number1),
            np.random.randint(2, max_number2),
        )
        if row_n / (real_nrows) < 1 / 2:  # not halfway ie. multiplication
            problem_string = f"{number1} x {number2}"
            sol_row_insert += ["", f"{number1*number2}"]
        else:
            problem_string = f"{number1} / {number2}"
            sol_row_insert += ["", f"{number1/number2:4.3f}"]
        row_insert += [problem_string, ""]
    table.append(row_insert)
    solution_table.append(sol_row_insert)

pandas_table = pd.DataFrame(table, columns=["Problem", "Answer"] * ncolumns)
pandas_table_sol = pd.DataFrame(
    solution_table, columns=["Problem", "Answer"] * ncolumns
)

# Convert to latex and save as mytable.tex
# col_format = "|"  # column lines
# for i in range(real_nrows):
#     col_format += "c|"
# latex_table = pandas_table.to_latex(index=False, column_format=col_format)


def latex_with_lines(df, *args, **kwargs):
    kwargs["column_format"] = "|".join(
        [""] + ["l"] * df.index.nlevels + ["r"] * df.shape[1] + [""]
    )
    res = df.to_latex(*args, **kwargs)
    return res.replace("\\\\\n", "\\\\ \\midrule\n")


latex_table = "\\LARGE\n" + latex_with_lines(pandas_table, index=False)
latex_table_sol = "\\LARGE\n" + latex_with_lines(pandas_table_sol, index=False)
f = open("mytable.tex", "w")
f.write(latex_table)
f.close()
f = open("mytable_sol.tex", "w")
f.write(latex_table_sol)
f.close()

# Write latex document that imports mytable.tex
f = open(pdf_name + ".tex", "w")
s = "\\documentclass{article}\n\\usepackage[a4paper, total={8in, 11in}]{geometry}\n\\usepackage{graphicx}\n\\renewcommand{\\arraystretch}{2.25}\n\\usepackage{booktabs}\n\\begin{document}\n\\input{mytable}\n\\end{document}"
f.write(s)
f.close()
f = open(pdf_name + "_solutions_" + ".tex", "w")
s = "\\documentclass{article}\n\\usepackage[a4paper, total={8in, 11in}]{geometry}\n\\usepackage{graphicx}\n\\renewcommand{\\arraystretch}{2.25}\n\\usepackage{booktabs}\n\\begin{document}\n\\input{mytable_sol}\n\\end{document}"
f.write(s)
f.close()

# Make the pdf with PDFLaTeX
pdfl = PDFLaTeX.from_texfile(pdf_name + ".tex")
pdf, log, completed_process = pdfl.create_pdf(keep_pdf_file=True, keep_log_file=True)
pdfl = PDFLaTeX.from_texfile(pdf_name + "_solutions_" + ".tex")
pdf, log, completed_process = pdfl.create_pdf(keep_pdf_file=True, keep_log_file=True)
