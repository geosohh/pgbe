from register import Register
import op

if __name__ == '__main__':
    register = Register()

    register.B = 0x00
    register.C = 0x01
    print("B=" + str(hex(register.B)) + "(" + str(register.B) + ")")
    print("C=" + str(hex(register.C)) + "(" + str(register.C) + ")")

    register.sub_bc(0x0100)

    print("B=" + str(hex(register.B)) + "(" + str(register.B) + ")")
    print("C=" + str(hex(register.C)) + "(" + str(register.C) + ")")
