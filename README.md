# rdiv
Standard Table 2-Resistor Divider Calculator

## Quick Start
### Requirements
* [numpy](https://numpy.org/install/)

See **Under the Hood** for why this uses NumPy. I'm (maybe unfairly) assuming you have NumPy installed if you are using this outside of Circuits 101.

### Usage
```
usage: Standard Table 2-Resistor Divider Calculator [-h]
                                                    [--table {E12,E24,E48,E96}]
                                                    [--prefer-over]
                                                    [--prefer-under]
                                                    Vin Vout

positional arguments:
  Vin                   divider input voltage
  Vout                  divider output voltage

optional arguments:
  -h, --help            show this help message and exit
  --table {E12,E24,E48,E96}
                        resistor table, defaults to E12
  --prefer-over         ignore solutions with lower Vout
  --prefer-under        ignore solutions with higher Vout
```

## Under the Hood
### Why NumPy?
I search a pairwise error grid to find the resistor pair (calculation is very fast, I promise). A pairwise grid of numbers is a matrix. NumPy is the go-to for dealing with matrices in Python.

### Why Build This?
Really, I was avoiding homework.

Technically, voltage dividers only prescribe a ratio (hence "divider"), but a standard form voltage divider needs 2 resistors. That's 1 equation, 2 unknowns. Futhermore, resistors are only available in certain values. This gives the circuit designer a knapsack problem to solve, instead of a degree of freedom to fix arbitrarily.

If you haven't seen [standard resistor tables](https://www.vishay.com/docs/31001/dectable.pdf), you very much should. They are a manufacturing and supply chain wonder.


Admittedly, it is good/quick enough to pick a few resistors and find their relevant pair, but again, I was avoiding homework.

### The Steps
1. Compute the divider resistor ratio, `k`
2. Constrain the resistor ratio to \(0,10\] using `log10`.
3. Compute the error ratio error matrix, `d = rtable*k-rtable.T`
4. Only look at the upper triangular portion of `d`, which is skew-symmetric
5. Ignore positive, negative, or no error entries, depending on user input
6. Convert to absolute error
7. Construct the "best column" - for each row, find the column with least absolute error
8. Find the "best row" - the row with least absolute error in the "best column"
9. The best column index gives R1, and the best row index gives R2
10. Scale R1 by the the original `k` order of magnitude
11. Print R1,R2

### The Math
Claim: Consider a solved minimum-error resistor ratio pair, R1 and R2. In implementation and in theory, if the ratio is multiplied by 10, the minimum-error R2 stays constant, and the minimum-error R1 is multiplied by 10. 

Proof:

![equation](https://latex.codecogs.com/gif.latex?%5Cfrac%7BV_o%7D%7BV_i%7D%20%3D%20%5Cfrac%7BR_2%7D%7BR_1&plus;R_2%7D%20%5Cto%20R_2%5Cleft%28%5Cfrac%7BV_i%7D%7BV_o%7D%20-%201%5Cright%20%29%20%3D%20R_1)

1. Notice that R1 scales with the ratio. That handles the "theory" part nicely
2. As for practice, resistor values come in "decades," or multiples of 10. For every resistor value listed in a table, a resistor with the same coefficient, but a different order of magnitude is available, e.g. 1.2->12->120->0.0012->etc. Such is the wonder of standard resistor tables.

Corollary: Any minimum-error voltage divider problem can be solved using only the coefficient of the desired resistor ratio represented in scientific notation without loss of generality.

## Acknowledgements
The resistor values used in this CLI were downloaded and regex'd from [this electronics-notes.com article](https://www.electronics-notes.com/articles/electronic_components/resistors/standard-resistor-values-e-series-e3-e6-e12-e24-e48-e96.php). Although resistor tables are standardized, the article embedded the values in an html table, which made automating input very easy.

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for more details.
