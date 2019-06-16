from sympy.algebras.quaternion import Quaternion
from sympy import symbols, cos, sin, atan2, asin, acos, init_printing, pretty
from sympy import trigsimp, pi, solve
from sympy.matrices import rot_axis1, rot_axis2, rot_axis3, Matrix

init_printing()

yaw   = symbols('yaw')
pitch = symbols('pitch')
roll  = symbols('roll')

# Basic system configuration
x_axis = [ 1, 0, 0 ]
y_axis = [ 0, 1, 0 ]
z_axis = [ 0, 0, 1 ]

# Direction cosines
n_yaw   = y_axis
n_pitch = x_axis
n_roll  = z_axis

def quaternion_from_angle(angle, dir_cos):
    # dir_cos should be a 3-dimension vector
    assert(len(dir_cos) == 3)

    return Quaternion(cos(angle/2),
                      sin(angle/2) * dir_cos[0],
                      sin(angle/2) * dir_cos[1],
                      sin(angle/2) * dir_cos[2])

q_yaw   = quaternion_from_angle(yaw, n_yaw)
q_pitch = quaternion_from_angle(pitch, n_pitch)
q_roll  = quaternion_from_angle(roll, n_roll)

q_final = q_roll * q_pitch * q_yaw;

print("q_yaw   =", pretty(q_yaw))
print("q_pitch =", pretty(q_pitch))
print("q_roll  =", pretty(q_roll))

print()
print("NOTE: Computation of final rotation is done with quaternions")
print("      multiplication in the reverse order of matrices in VLC because")
print("      of matrices being transposed in the C code but uploaded in the")
print("      column major order.")
print("q_final =", pretty(q_final))
print()

print(" -- rotation_matrix --\n")
print("NOTE: In comparison with VLC's matrices, they are transposed because")
print("      they are in row-major order instead of colum-major order.")


print()
print(" -- q_yaw (y_rot) --\n")
print(pretty(q_yaw.to_rotation_matrix()))

print()
print(" -- q_pitch (x_rot) --\n")
print(pretty(q_pitch.to_rotation_matrix()))

print()
print(" -- q_roll (z_rot) --\n")
print(pretty(q_roll.to_rotation_matrix()))

print()
print(" -- Identification to get back Euler angles from quaternion --")

print()
print(" => use a generic quaternion (qw, qz, qy, qz)")

g_qw, g_qx, g_qy, g_qz = symbols("gw gx gy gz")
generic_quaternion = Quaternion(g_qw, g_qx, g_qy, g_qz)
print()
print(generic_quaternion)

print()
print(" => generate rotation matrix from angles")

m_yaw = rot_axis2(yaw)
m_pitch = rot_axis1(pitch)
m_roll = rot_axis3(roll)

print()
print(" -- m_yaw (y_rot) --\n")
print(pretty(m_yaw))

print()
print(" -- m_pitch (x_rot) --\n")
print(pretty(m_pitch))

print()
print(" -- m_roll (z_rot) --\n")
print(pretty(m_roll))

print()
print(" => multiply rotation in the correct order")

m_final = m_roll * m_pitch * m_yaw

print()
print(pretty(m_final))

print()
print(" => identify the matrix with the quaternion's generated one")

expr = m_final - generic_quaternion.to_rotation_matrix()
print()
print(pretty(expr))

print()
print(" -- Conversion from Quaternion to Euler --\n")

print(" => solve the previous equation")
print("NOTE: No computer algebra system can solve this, so you have to work it")
print("      out yourself.")

#values = solve(expr, g_qw, g_qx, g_qy, g_qz, warn=True, )
#
#print()
#print(pretty(values))



#q = q_final
#c_yaw   = atan2(2 * (q.d * q.a + q.b * q.c),
#                1 - 2 * (q.c * q.c + q.d * q.d))
#c_pitch = asin(2 * (q.c * q.a - q.d * q.c))
#c_roll  = atan2(2 * (q.b * q.a + q.c * q.d),
#                1 - 2 * (q.b * q.b + q.c * q.c))
#
#c_yaw   = trigsimp(c_yaw)
#c_pitch = trigsimp(c_pitch)
#c_roll  = trigsimp(c_roll)
#
#
#print()
#print("yaw   =", c_yaw)
#
#print()
#print("pitch =", c_pitch)
#e = {yaw: 0, pitch: pi/4, roll: 0}
#print(e)
#print("pitch(45) = ", c_pitch.evalf(subs=e))
#print("pitch(90) = ", c_pitch.evalf(subs={yaw: 0, pitch: pi/2, roll: 0}))
#
#print()
#print("roll  =", c_roll)
#print("roll(45) = ", c_roll.evalf(subs={yaw: 0, pitch: 0, roll: pi/4}))
#print("roll(90) = ", c_roll.evalf(subs={yaw: 0, pitch: 0, roll: pi/2}))
#
#
##print(pretty(q_final.to_rotation_matrix()))
#
