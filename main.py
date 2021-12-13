
from signal import Signal

un = Signal(compute=lambda x: 1 if 0 <= x else 0) # UNIT STEP SIGNAL
xn = Signal(compute=lambda x: 0.85**x) * un
hn = un - (un >> 6)


# FOLDING
(hn >> 3).plot(name="y[n]") # RIGHT SHIFT
(hn << 3).plot(name="y[n]") # LEFT SHIFT

# SCALING
(xn * 5).plot(name="y[n]")

# ADDITION
(hn + xn).plot(name="y[n]")

# SUBTRACTION
(xn - xn).plot(name="y[n]")

# MULTIPLICATION
(xn * hn).plot(name="y[n]")

# DIVISION
(xn / (hn*2)).plot(name="y[n]")

# CONVOLUTION
hn.bounds = range(0, 6)
(xn ** hn).plot(name="y[n]", bounds=range(-2, 21))