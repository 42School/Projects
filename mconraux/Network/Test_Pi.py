__author__ = 'epoch'

import sys
#
# scale = 1000
# maxarr = 2800
# arrinit = 2000
# carry = 0
# arr = [arrinit] * (maxarr + 1)
# for i in xrange(maxarr, 1, -14):
# total = 0
#     for j in xrange(i, 0, -1):
#         total = (total * j) + (scale * arr[j])
#         arr[j] = total % ((j * 2) - 1)
#         total = total / ((j * 2) - 1)
#     sys.stdout.write("%04d" % (carry + (total / scale)))
#     carry = total % scale

def arccot(x, unity):
    sum = xpower = unity // x
    n = 3
    sign = -1
    while 1:
        xpower = xpower // (x * x)
        term = xpower // n
        if not term:
            break
        sum += sign * term
        sign = -sign
        n += 2
    return sum


def pi(digits):
    unity = 10 ** (digits + 10)
    pi = 4 * (4 * arccot(5, unity) - arccot(239, unity))
    return pi // 10 ** 10


if len(sys.argv) >= 2:
    n = sys.argv[1]
else:
    n = 10000

print pi(n)