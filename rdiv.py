#!/usr/bin/env python3
"""
Compute standard resistor divider pair (CLI).

(c) Marion Anderson, 2021
Provided under the MIT License.
"""
from argparse import ArgumentParser
from math import inf, floor, log10
from sys import exit

from numpy import (argmin, array, fill_diagonal, newaxis, tril, triu)

# Resistor Values (bless up for regex html downloads)
# src: https://www.electronics-notes.com/articles/electronic_components/resistors/standard-resistor-values-e-series-e3-e6-e12-e24-e48-e96.php
E12 = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]
E24 = [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0, 3.3, 3.6,
       3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1]
E48 = [1.0, 1.05, 1.1, 1.15, 1.21, 1.27, 1.33, 1.4, 1.47, 1.54, 1.62, 1.69,
       1.78, 1.87, 1.96, 2.05, 2.15, 2.26, 2.37, 2.49, 2.61, 2.74, 2.87, 3.01,
       3.16, 3.32, 3.48, 3.65, 3.83, 4.02, 4.22, 4.42, 4.64, 4.87, 5.11, 5.36,
       5.62, 5.9, 6.19, 6.49, 6.81, 7.15, 7.5, 7.87, 8.25, 8.66, 9.09, 9.53]
E96 = [1.0, 1.02, 1.05, 1.07, 1.1, 1.13, 1.15, 1.18, 1.21, 1.24, 1.27, 1.3,
       1.33, 1.37, 1.4, 1.43, 1.47, 1.5, 1.54, 1.62, 1.65, 1.69, 1.74, 1.78,
       1.82, 1.87, 1.91, 1.96, 2.0, 2.05, 2.1, 2.16, 2.21, 2.26, 2.32, 2.37,
       2.43, 2.49, 2.55, 2.61, 2.67, 2.74, 2.8, 2.87, 2.94, 3.01, 3.09, 3.16,
       3.24, 3.32, 3.4, 3.48, 3.57, 3.65, 3.74, 3.83, 3.92, 4.02, 4.12, 4.22,
       4.32, 4.42, 4.53, 4.64, 4.75, 4.87, 4.99, 5.11, 5.23, 5.36, 5.49, 5.62,
       5.76, 5.9, 6.04, 6.19, 6.34, 6.49, 6.65, 6.98, 7.15, 7.32, 7.5, 7.68,
       7.87, 8.06, 8.25, 8.45, 8.66, 8.87, 9.09, 9.31, 9.53, 9.76]

parser = ArgumentParser('Standard Table 2-Resistor Divider Calculator')
parser.add_argument('Vin', type=float, help='divider input voltage')
parser.add_argument('Vout', type=float, help='divider output voltage')
parser.add_argument('--table', choices=['E12','E24','E48','E96'],
                    default='E12', help='resistor table, defaults to E12')
parser.add_argument('--prefer-over', action='store_true',
                    help='ignore solutions with lower Vout')
parser.add_argument('--prefer-under', action='store_true',
                    help='ignore solutions with higher Vout')

if __name__ == '__main__':
    # Parse Args
    args = parser.parse_args()
    if args.prefer_over and args.prefer_under:
        print('--prefer-over and --prefer-under are mutually exclusive')
        exit(1)
    Vin = args.Vin
    Vout = args.Vout
    rtable = eval(args.table)
    rtable += [10*v for v in rtable]  # include 10x higher resistors

    # Compute Resistor Ideal Ratio
    mult = Vin/Vout - 1
    powOf10 = floor(log10(mult))  # resistor tables are for 1 power of 10
    mult = mult * 10**(-powOf10)

    # Construct Difference-From-Ideal-R Matrix
    res_arr = array(rtable)[:,newaxis]             # convert to col vec
    diffmat = triu(mult*res_arr - res_arr.T)       # absolute difference is symm
    ignoremat = tril(diffmat+inf)                  # ignore below diag portion
    fill_diagonal(ignoremat, 0)
    diffmat += ignoremat
    if args.prefer_over:   # ignore voltage below desired Vout
        diffmat[diffmat<0] = inf
    if args.prefer_under:  # ignore voltage above desired Vout
        diffmat[diffmat>0] = inf
    diffmat = abs(diffmat)

    # Find Best R Pair
    mincols = argmin(diffmat,axis=1).astype('int')      # ndx of best for ech
    r1cands = diffmat[range(mincols.shape[0]),mincols]  # min rndx for each r
    minrows = argmin(r1cands).astype('int')             # best row

    # Output
    r1 = rtable[mincols[minrows]]  # top resistor
    r1 *= 10**powOf10
    r2 = rtable[minrows]           # bottom resistor
    Vo = Vin * r2 / (r1 + r2)      # actual vout
    print('R1={}, R2={}, Vout={}'.format(r1, r2, Vo))

