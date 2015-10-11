import numpy as np

pts = np.zeros([11, 3])
pts[0, :] = [-1, -1, -1]
pts[1, :] = [ 1, -1, -1]
pts[2, :] = [ 1,  1, -1]
pts[3, :] = [-1,  1, -1]
pts[4, :] = [-1, -1,  1]
pts[5, :] = [ 1, -1,  1]
pts[6, :] = [ 1,  1,  1]
pts[7, :] = [-1,  1,  1]
pts[8, :] = [-0.5, -0.5, -1]
pts[9, :] = [ 0.5, -0.5, -1]
pts[10, :] = [0, 0.5, -1]

# Helper functions
def conjugate(q):
	'''conjugate of q'''
	return [q[0]] + [-i for i in q[1:]]

def quat(point):
	'''make a 3D point r into a quarternion'''
	return [0] + point

def point(quat):
	'''make a quarternion q into a 3d point'''
	return quat[1:]

# 1.2
def quatmult(q1, q2):
	# quaternion multiplication
	out = [0, 0, 0, 0] # output array to hold the result
	out[0] = q1[0]*q2[0] - q1[1]*q2[1] - q1[2]*q2[2] - q1[3]*q2[3]
	out[1] = q1[0]*q2[1] + q1[1]*q2[0] + q1[2]*q2[3] - q1[3]*q2[2]
	out[2] = q1[0]*q2[2] - q1[1]*q2[3] + q1[2]*q2[0] + q1[3]*q2[1]
	out[3] = q1[0]*q2[3] + q1[1]*q2[2] - q1[2]*q2[1] + q1[3]*q2[0]
	return out

def quat_rotate(p, q):
	'''rotate p by q'''
	return quatmult(quatmult(q, p), conjugate(q))

radian_neg15 = float(-30 / 2) / 180 * np.pi
rotate_quat = [np.cos(radian_neg15), 0, np.sin(radian_neg15), 0]

pos1 = [0, 0, -5]
camera_positions = [quat(pos1)]
for i in range(3):
	new_pos = quat_rotate(camera_positions[-1], rotate_quat)
	camera_positions += [new_pos]

q1, q2, q3, q4 = camera_positions
pos2 = point(q2)
pos3 = point(q3)
pos4 = point(q4)
print 'pos1 =', pos1
print 'pos2 =', pos2
print 'pos3 =', pos3
print 'pos4 =', pos4



