from sympy.algebras.quaternion import Quaternion
from sympy import symbols, cos, sin, init_printing, pretty

init_printing()

yaw   = symbols('yaw')
pitch = symbols('pitch')
roll  = symbols('roll')

# Direction cosines
n_yaw   = [ 0, 1, 0 ]
n_pitch = [ 1, 0, 0 ]
n_roll  = [ 0, 0, 1 ]

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

q_final = q_yaw * q_pitch * q_roll

print("q_yaw   =", pretty(q_yaw))
print("q_pitch =", pretty(q_pitch))
print("q_roll  =", pretty(q_roll))
print("q_final =", pretty(q_final))
print("rotation_matrix:")

print()
print("q_yaw (y_rot)")
print(pretty(q_yaw.to_rotation_matrix()))

print()
print("q_pitch (x_rot)")
print(pretty(q_pitch.to_rotation_matrix()))

print()
print("q_roll (z_rot)")
print(pretty(q_roll.to_rotation_matrix()))

print()
print("NOTE: In comparison with VLC's matrices, they are transposed because")
print("      they are in row-major order instead of colum-major order.") 

#print(pretty(q_final.to_rotation_matrix()))

