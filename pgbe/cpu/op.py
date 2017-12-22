# OPCODES 0x
def code_00(register):
    pass


def code_01(register):
    pass


def code_02(register):
    """ LD (BC),A - Stores reg at the address in BC """
    # TODO after memory is implemented
    pass


def code_03(register):
    pass


def code_04(register):
    pass


def code_05(register):
    pass


def code_06(register, d8):
    """ LD B,d8 """
    register.B = d8


def code_07(register):
    pass


def code_08(register):
    pass


def code_09(register):
    pass


def code_0a(register):
    """ LD A,(BC) - Load reg with the value at the address in BC """
    # TODO after memory is implemented
    pass


def code_0b(register):
    pass


def code_0c(register):
    pass


def code_0d(register):
    pass


def code_0e(register, d8):
    """ LD C,d8 """
    register.C = d8


def code_0f(register):
    pass


# OPCODES 1x
def code_10(register):
    pass

def code_11(register):
    pass


def code_12(register):
    """ LD (DE),A - Stores reg at the address in DE """
    # TODO after memory is implemented
    pass


def code_13(register):
    pass

def code_14(register):
    pass

def code_15(register):
    pass


def code_16(register, d8):
    """ LD D,d8 """
    register.D = d8


def code_17(register):
    pass

def code_18(register):
    pass

def code_19(register):
    pass


def code_1a(register):
    """ LD A,(DE) - Load reg with the value at the address in DE """
    # TODO after memory is implemented
    pass


def code_1b(register):
    pass

def code_1c(register):
    pass

def code_1d(register):
    pass


def code_1e(register, d8):
    """ LD E,d8 """
    register.E = d8


def code_1f(register):
    pass

# OPCODES 2x
def code_20(register):
    pass

def code_21(register):
    pass

def code_22(register):
    pass

def code_23(register):
    pass

def code_24(register):
    pass

def code_25(register):
    pass


def code_26(register, d8):
    """ LD H,d8 """
    register.H = d8


def code_27(register):
    pass

def code_28(register):
    pass

def code_29(register):
    pass

def code_2a(register):
    pass

def code_2b(register):
    pass

def code_2c(register):
    pass

def code_2d(register):
    pass


def code_2e(register, d8):
    """ LD L,d8 """
    register.L = d8


def code_2f(register):
    pass

# OPCODES 3x
def code_30(register):
    pass

def code_31(register):
    pass

def code_32(register):
    pass

def code_33(register):
    pass

def code_34(register):
    pass

def code_35(register):
    pass


def code_36(register, d8):
    """ LD (HL),d8 - Stores d8 at the address in HL """
    # TODO after memory is implemented
    pass


def code_37(register):
    pass

def code_38(register):
    pass

def code_39(register):
    pass


def code_3a(register):
    """ LD A,(HL-) or LD A,(HLD) or LDD A,(HL) - Put value at address HL into A. Decrement HL """
    # TODO after memory is implemented
    register.HL -= 1  # TODO: what if HL is already 0x0000?
    pass


def code_3b(register):
    pass

def code_3c(register):
    pass

def code_3d(register):
    pass


def code_3e(register, d8):
    """ LD A,d8 """
    register.A = d8


def code_3f(register):
    pass


# OPCODES 4x
def code_40(register):
    """ LD B,B (might be a newbie question but... why?) """
    register.B = register.B


def code_41(register):
    """ LD B,C """
    register.B = register.C


def code_42(register):
    """ LD B,D """
    register.B = register.D


def code_43(register):
    """ LD B,E """
    register.B = register.E


def code_44(register):
    """ LD B,H """
    register.B = register.H


def code_45(register):
    """ LD B,L """
    register.B = register.L


def code_46(register):
    """ LD B,(HL) - Load reg with the value at the address in HL """
    # TODO after memory is implemented
    pass


def code_47(register):
    """ LD B,A """
    register.B = register.A


def code_48(register):
    """ LD C,B """
    register.C = register.B


def code_49(register):
    """ LD C,C (might be a newbie question but... why?) """
    register.C = register.C


def code_4a(register):
    """ LD C,D """
    register.C = register.D


def code_4b(register):
    """ LD C,E """
    register.C = register.E


def code_4c(register):
    """ LD C,H """
    register.C = register.H


def code_4d(register):
    """ LD C,L """
    register.C = register.L


def code_4e(register):
    """ LD C,(HL) - Load reg with the value at the address in HL """
    # TODO after memory is implemented
    pass


def code_4f(register):
    """ LD C,A """
    register.C = register.A


# OPCODES 5x
def code_50(register):
    """ LD D,B """
    register.D = register.B


def code_51(register):
    """ LD D,C """
    register.D = register.C


def code_52(register):
    """ LD D,D (might be a newbie question but... why?) """
    register.D = register.D


def code_53(register):
    """ LD D,E """
    register.D = register.E


def code_54(register):
    """ LD D,H """
    register.D = register.H


def code_55(register):
    """ LD D,L """
    register.D = register.L


def code_56(register):
    """ LD D,(HL) - Load reg with the value at the address in HL """
    # TODO after memory is implemented
    pass


def code_57(register):
    """ LD D,A """
    register.D = register.A


def code_58(register):
    """ LD E,B """
    register.E = register.B


def code_59(register):
    """ LD E,C """
    register.E = register.C


def code_5a(register):
    """ LD E,D """
    register.E = register.D


def code_5b(register):
    """ LD E,E (might be a newbie question but... why?) """
    register.E = register.E


def code_5c(register):
    """ LD E,H """
    register.E = register.H


def code_5d(register):
    """ LD E,L """
    register.E = register.L


def code_5e(register):
    """ LD E,(HL) - Load reg with the value at the address in HL """
    # TODO after memory is implemented
    pass


def code_5f(register):
    """ LD E,A """
    register.E = register.A


# OPCODES 6x
def code_60(register):
    """ LD H,B """
    register.H = register.B


def code_61(register):
    """ LD H,C """
    register.H = register.C


def code_62(register):
    """ LD H,D """
    register.H = register.D


def code_63(register):
    """ LD H,E """
    register.H = register.E


def code_64(register):
    """ LD H,H (might be a newbie question but... why?) """
    register.H = register.H


def code_65(register):
    """ LD H,L """
    register.H = register.L


def code_66(register):
    """ LD H,(HL) - Load reg with the value at the address in HL """
    # TODO after memory is implemented
    pass


def code_67(register):
    """ LD H,A """
    register.H = register.A


def code_68(register):
    """ LD L,B """
    register.L = register.B


def code_69(register):
    """ LD L,C """
    register.L = register.C


def code_6a(register):
    """ LD L,D """
    register.L = register.D


def code_6b(register):
    """ LD L,E """
    register.L = register.E


def code_6c(register):
    """ LD L,H """
    register.L = register.H


def code_6d(register):
    """ LD L,L (might be a newbie question but... why?) """
    register.L = register.L


def code_6e(register):
    """ LD L,(HL) - Load reg with the value at the address in HL """
    # TODO after memory is implemented
    pass


def code_6f(register):
    """ LD L,A """
    register.L = register.A


# OPCODES 7x
def code_70(register):
    """ LD (HL),B - Stores reg at the address in HL """
    # TODO after memory is implemented
    pass


def code_71(register):
    """ LD (HL),C - Stores reg at the address in HL """
    # TODO after memory is implemented
    pass


def code_72(register):
    """ LD (HL),D - Stores reg at the address in HL """
    # TODO after memory is implemented
    pass


def code_73(register):
    """ LD (HL),E - Stores reg at the address in HL """
    # TODO after memory is implemented
    pass


def code_74(register):
    """ LD (HL),H - Stores reg at the address in HL """
    # TODO after memory is implemented
    pass


def code_75(register):
    """ LD (HL),L - Stores reg at the address in HL """
    # TODO after memory is implemented
    pass


def code_76(register):
    pass


def code_77(register):
    """ LD (HL),A - Stores reg at the address in HL """
    # TODO after memory is implemented
    pass


def code_78(register):
    """ LD A,B """
    register.A = register.B


def code_79(register):
    """ LD A,C """
    register.A = register.C


def code_7a(register):
    """ LD A,D """
    register.A = register.D


def code_7b(register):
    """ LD A,E """
    register.A = register.E


def code_7c(register):
    """ LD A,H """
    register.A = register.H


def code_7d(register):
    """ LD A,L """
    register.A = register.L


def code_7e(register):
    """ LD A,(HL) - Load reg with the value at the address in HL """
    # TODO after memory is implemented
    pass


def code_7f(register):
    """ LD A,A (might be a newbie question but... why?) """
    register.A = register.A


# OPCODES 8x
def code_80(register):
    pass

def code_81(register):
    pass

def code_82(register):
    pass

def code_83(register):
    pass

def code_84(register):
    pass

def code_85(register):
    pass

def code_86(register):
    pass

def code_87(register):
    pass

def code_88(register):
    pass

def code_89(register):
    pass

def code_8a(register):
    pass

def code_8b(register):
    pass

def code_8c(register):
    pass

def code_8d(register):
    pass

def code_8e(register):
    pass

def code_8f(register):
    pass

# OPCODES 9x
def code_90(register):
    pass

def code_91(register):
    pass

def code_92(register):
    pass

def code_93(register):
    pass

def code_94(register):
    pass

def code_95(register):
    pass

def code_96(register):
    pass

def code_97(register):
    pass

def code_98(register):
    pass

def code_99(register):
    pass

def code_9a(register):
    pass

def code_9b(register):
    pass

def code_9c(register):
    pass

def code_9d(register):
    pass

def code_9e(register):
    pass

def code_9f(register):
    pass

# OPCODES Ax
def code_a0(register):
    pass

def code_a1(register):
    pass

def code_a2(register):
    pass

def code_a3(register):
    pass

def code_a4(register):
    pass

def code_a5(register):
    pass

def code_a6(register):
    pass

def code_a7(register):
    pass

def code_a8(register):
    pass

def code_a9(register):
    pass

def code_aa(register):
    pass

def code_ab(register):
    pass

def code_ac(register):
    pass

def code_ad(register):
    pass

def code_ae(register):
    pass

def code_af(register):
    pass

# OPCODES Bx
def code_b0(register):
    pass

def code_b1(register):
    pass

def code_b2(register):
    pass

def code_b3(register):
    pass

def code_b4(register):
    pass

def code_b5(register):
    pass

def code_b6(register):
    pass

def code_b7(register):
    pass

def code_b8(register):
    pass

def code_b9(register):
    pass

def code_ba(register):
    pass

def code_bb(register):
    pass

def code_bc(register):
    pass

def code_bd(register):
    pass

def code_be(register):
    pass

def code_bf(register):
    pass

# OPCODES Cx
def code_c0(register):
    pass

def code_c1(register):
    pass

def code_c2(register):
    pass

def code_c3(register):
    pass

def code_c4(register):
    pass

def code_c5(register):
    pass

def code_c6(register):
    pass

def code_c7(register):
    pass

def code_c8(register):
    pass

def code_c9(register):
    pass

def code_ca(register):
    pass

def code_cb(register):
    pass

def code_cc(register):
    pass

def code_cd(register):
    pass

def code_ce(register):
    pass

def code_cf(register):
    pass

# OPCODES Dx
def code_d0(register):
    pass

def code_d1(register):
    pass

def code_d2(register):
    pass

def code_d3(register):
    pass

def code_d4(register):
    pass

def code_d5(register):
    pass

def code_d6(register):
    pass

def code_d7(register):
    pass

def code_d8(register):
    pass

def code_d9(register):
    pass

def code_da(register):
    pass

def code_db(register):
    pass

def code_dc(register):
    pass

def code_dd(register):
    pass

def code_de(register):
    pass

def code_df(register):
    pass

# OPCODES Ex
def code_e0(register):
    pass

def code_e1(register):
    pass


def code_e2(register):
    """ LD (C),A or LD ($FF00+C),A - Put A into address ($FF00 + register C) """
    # TODO after memory is implemented
    pass


def code_e3(register):
    pass

def code_e4(register):
    pass

def code_e5(register):
    pass

def code_e6(register):
    pass

def code_e7(register):
    pass

def code_e8(register):
    pass

def code_e9(register):
    pass


def code_ea(register,a16):
    """ LD (a16),A - Stores reg at the address in a16 (least significant byte first) """
    # TODO after memory is implemented
    pass


def code_eb(register):
    pass

def code_ec(register):
    pass

def code_ed(register):
    pass

def code_ee(register):
    pass

def code_ef(register):
    pass

# OPCODES Fx
def code_f0(register):
    pass

def code_f1(register):
    pass


def code_f2(register):
    """ LD A,(C) or LD A,($FF00+C) - Put value at address ($FF00 + register C) into A """
    # TODO after memory is implemented
    pass


def code_f3(register):
    pass

def code_f4(register):
    pass

def code_f5(register):
    pass

def code_f6(register):
    pass

def code_f7(register):
    pass

def code_f8(register):
    pass

def code_f9(register):
    pass


def code_fa(register,a16):
    """ LD A,(a16) - Load reg with the value at the address in a16 (least significant byte first) """
    # TODO after memory is implemented
    pass


def code_fb(register):
    pass

def code_fc(register):
    pass

def code_fd(register):
    pass

def code_fe(register):
    pass

def code_ff(register):
    pass
