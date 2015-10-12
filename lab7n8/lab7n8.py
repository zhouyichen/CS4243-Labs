import numpy as np
import matplotlib.pyplot as plt

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
camera_positions = [pos1, pos2, pos3, pos4]

# 1.3
def quat2rot(q):
	q0, q1, q2, q3 = q
	q0sq = q0 * q0
	q1sq = q1 * q1
	q2sq = q2 * q2
	q3sq = q3 * q3
	q0q1 = q0 * q1
	q0q2 = q0 * q2
	q0q3 = q0 * q3
	q1q2 = q1 * q2
	q1q3 = q1 * q3
	q2q3 = q2 * q3
	return np.matrix([
		[q0sq + q1sq - q2sq - q3sq, 2 * (q1q2 - q0q3), 2 * (q1q3 + q0q2)],
		[2 * (q1q2 + q0q3), q0sq + q2sq - q1sq - q3sq, 2 * (q2q3 - q0q1)],
		[2 * (q1q3 - q0q2), 2 * (q2q3 + q0q1), q0sq + q3sq - q1sq - q2sq]])

radian_15 = float(30 / 2) / 180 * np.pi
rotation_quat = [np.cos(radian_15), 0, np.sin(radian_15), 0]
rotation_mat = quat2rot(rotation_quat)
quatmat_1 = np.identity(3)
camera_orientations = [quatmat_1]
for i in range(3):
	new_orientation = rotation_mat * camera_orientations[-1]
	camera_orientations += [new_orientation]

quatmat_1, quatmat_2, quatmat_3, quatmat_4 = camera_orientations
print 'quatmat_1 ='
print quatmat_1
print 'quatmat_2 ='
print quatmat_2
print 'quatmat_3 ='
print quatmat_3
print 'quatmat_4 ='
print quatmat_4

# Part 2
u_0 = 0
v_0 = 0
b_u = 1
b_v = 1
k_u = 1
k_v = 1
f = 1

def perspective_projection(s_p, t_f, i_f, j_f, k_f):
	sp_tf = s_p - t_f
	ufp = f * float(np.dot(sp_tf, i_f)) / np.dot((sp_tf), k_f) * b_u + u_0
	vfp = f * float(np.dot(sp_tf, j_f)) / np.dot((sp_tf), k_f) * b_v + v_0
	return [ufp, vfp]

def orthographic_projection(s_p, t_f, i_f, j_f, k_f):
	sp_tf = s_p - t_f
	ufp = float(np.dot(sp_tf, i_f)) * b_u + u_0
	vfp = float(np.dot(sp_tf, j_f)) * b_v + v_0
	return [ufp, vfp]	

def plot_projection(proj_model, axis):
	fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
	subplots = [ax1, ax2, ax3, ax4]
	for i in range(4):
		position = camera_positions[i]
		i_f, j_f, k_f = np.array(camera_orientations[i])
		points = [proj_model(pt, position, i_f, j_f, k_f) for pt in pts]
		subplot = subplots[i]
		subplot.set_xlim([-axis, axis])
		subplot.set_ylim([-axis, axis])
		subplot.set_title('frame ' + str(i + 1))
		for pt in points:
			subplot.plot(pt[0], pt[1], 'bo')
	plt.tight_layout()
	return fig

perspective_plot = plot_projection(perspective_projection, 0.4)
orthographic_plot = plot_projection(orthographic_projection, 2)
plt.show()


