from register import Register
import op

if __name__ == '__main__':
    register = Register()

    print("B="+str(register.B))
    op.code_06(register,10)
    print("B="+str(register.B))
