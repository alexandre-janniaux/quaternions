from sympy.algebras.quaternion import Quaternion
from sympy import symbols, cos, sin, atan2, asin, acos, init_printing, pretty
from sympy import trigsimp, pi, solve, Eq, refine
from sympy.matrices import rot_axis1, rot_axis2, rot_axis3, Matrix

init_printing()

yaw   = symbols('yaw', real=True)
pitch = symbols('pitch', real=True)
roll  = symbols('roll', real=True)

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

# adding a minus sign here transpose the resulting matrix
q_yaw   = quaternion_from_angle(yaw, n_yaw)
q_pitch = quaternion_from_angle(pitch, n_pitch)
q_roll  = quaternion_from_angle(-roll, n_roll)

q_final = q_roll * q_pitch * q_yaw

print("q_yaw   =", pretty(q_yaw))
print("q_pitch =", pretty(q_pitch))
print("q_roll  =", pretty(q_roll))


s_yaw, c_yaw = symbols(['s_yaw', 'c_yaw'])
s_pitch, c_pitch = symbols(['s_pitch', 'c_pitch'])
s_roll, c_roll = symbols(['s_roll', 'c_roll'])

q_final_sub = (q_final
               .subs(sin(yaw/2), s_yaw)
               .subs(cos(yaw/2), c_yaw)
               .subs(sin(pitch/2), s_pitch)
               .subs(cos(pitch/2), c_pitch)
               .subs(sin(roll/2), s_roll)
               .subs(cos(roll/2), c_roll))

print()
print("NOTE: Computation of final rotation is done with quaternions")
print("      multiplication in the reverse order of matrices in VLC because")
print("      of matrices being transposed in the C code but uploaded in the")
print("      column major order.")
print()

print("    q[3] = {};".format(q_final_sub.a))
print("    q[0] = {};".format(q_final_sub.b))
print("    q[1] = {};".format(q_final_sub.c))
print("    q[2] = {};".format(q_final_sub.d))
print()

print(" -- rotation_matrix --")

print()
print("NOTE: Matrix here are appearing as transposed because they are written")
print("      in column-major order, just like OpenGL and D3D11 is expecting them")
print()

print()
print(" -- q_yaw (y_rot) --\n")
print(pretty(q_yaw.to_rotation_matrix().transpose()))

print()
print(" -- q_pitch (x_rot) --\n")
print(pretty(q_pitch.to_rotation_matrix().transpose()))

print()
print(" -- q_roll (z_rot) --\n")
print(pretty(q_roll.to_rotation_matrix()))

print()
print(" -- q_final(0, 45, 45) --\n")
print(pretty(q_final.to_rotation_matrix()
    .subs(yaw, 0)
    .subs(pitch, pi / 4)
    .subs(roll, pi / 4)
    .evalf()))

print()
print(" -- final matrix(0, 45, 45) -- ")
m_yaw   = q_yaw.to_rotation_matrix()
m_pitch = q_pitch.to_rotation_matrix()
m_roll  = q_roll.to_rotation_matrix()
m_final = m_roll * m_pitch * m_yaw
print(pretty(m_final
             .subs(yaw, pi / 2)
             .subs(pitch, pi / 4)
             .subs(roll, pi / 4)
             .evalf()))

print()
print(" -- Identification to get back Euler angles from quaternion --")

print()
print(" => use a generic quaternion (qw, qz, qy, qz)")

g_qw, g_qx, g_qy, g_qz = symbols("gw gx gy gz", real=True)
generic_quaternion = Quaternion(g_qw, g_qx, g_qy, g_qz)
quat_norm = g_qw**2 + g_qx**2 + g_qy**2 + g_qz**2
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

print()
print(pretty(Eq(m_final, generic_quaternion.to_rotation_matrix()) \
            .subs(quat_norm, 1)))

#print()
#print(" -- Conversion from Quaternion to Euler --\n")
#
#print(" => solve the previous equation")
#print("NOTE: No computer algebra system can solve this, so you have to work it")
#print("      out yourself.")
#
#expr_base = m_final - generic_quaternion.to_rotation_matrix()
#expr = trigsimp(expr_base).subs(quat_norm, 1)
#
#print()
#print(pretty(expr))
#
#values = solve([
#    expr, hint_quat,
#    # yaw >= 0, yaw <= 360,
#    # pitch >= 0, pitch <= 360,
#    # roll >= 0, roll <= 360,
#], [yaw, pitch, roll], warn=True)
#
#print()
#print(pretty(values))
#
#print(values)
#
#print()
#print(" => simplify")
#
#print()
#print(values[0][0].rewrite(atan2))

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
