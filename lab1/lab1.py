import numpy as np
import numpy.linalg as la

file = open("data.txt")
data = np.genfromtxt(file, delimiter=",")
file.close()

print "Data =\n", data
print

def helper(m):
	zeros = [0, 0, 0]
	result = []
	for row in m:
		result.extend([row.tolist() + [1] + zeros, zeros + row.tolist() + [1]])
	return result

M = np.matrix(helper(data[:, :2]))
b = np.matrix(data[:,2:].flatten()).transpose()
print "M =\n", M
print
print "b =\n", b
print

a, e, r, s = la.lstsq(M, b)
print "a =\n", a
print
print "sum-squared error between M*a and b =", la.norm(M * a - b) ** 2
print
print "residue computed by la.lstsq e =", e