"""
CPU
"""


from cpu.register import Register
import cpu.op


class CPU:
    def __init__(self):
        self.prefix_cb = False

        self.halted = False  # for 76 (HALT)
        self.stopped = False  # for 10 (STOP)
        self.interrupts_enabled = False  # for F3 (DI) and FB (EI)
        self.disable_interrupts_requested = False  # for F3 (DI) and FB (EI)

        self.register = Register()
    
    def execute_operation(self, data):
        """
        Executes the operation requested by the given data.

        :param data: List of 8-bit values, where data[0] is the operation code and the additional values are the
                     operation parameters.
        :return:
        """
        opcode = data.pop(0)
        if self.prefix_cb:
            op_cb_set[opcode](self, data)
        else:
            op_set[opcode](self,data)


op_set = {
    "00": cpu.op.code_00,    "01": cpu.op.code_01,    "02": cpu.op.code_02,    "03": cpu.op.code_03,
    "04": cpu.op.code_04,    "05": cpu.op.code_05,    "06": cpu.op.code_06,    "07": cpu.op.code_07,
    "08": cpu.op.code_08,    "09": cpu.op.code_09,    "0a": cpu.op.code_0a,    "0b": cpu.op.code_0b,
    "0c": cpu.op.code_0c,    "0d": cpu.op.code_0d,    "0e": cpu.op.code_0e,    "0f": cpu.op.code_0f,
    
    "10": cpu.op.code_10,    "11": cpu.op.code_11,    "12": cpu.op.code_12,    "13": cpu.op.code_13,
    "14": cpu.op.code_14,    "15": cpu.op.code_15,    "16": cpu.op.code_16,    "17": cpu.op.code_17,
    "18": cpu.op.code_18,    "19": cpu.op.code_19,    "1a": cpu.op.code_1a,    "1b": cpu.op.code_1b,
    "1c": cpu.op.code_1c,    "1d": cpu.op.code_1d,    "1e": cpu.op.code_1e,    "1f": cpu.op.code_1f,

    "20": cpu.op.code_20,    "21": cpu.op.code_21,    "22": cpu.op.code_22,    "23": cpu.op.code_23,
    "24": cpu.op.code_24,    "25": cpu.op.code_25,    "26": cpu.op.code_26,    "27": cpu.op.code_27,
    "28": cpu.op.code_28,    "29": cpu.op.code_29,    "2a": cpu.op.code_2a,    "2b": cpu.op.code_2b,
    "2c": cpu.op.code_2c,    "2d": cpu.op.code_2d,    "2e": cpu.op.code_2e,    "2f": cpu.op.code_2f,

    "30": cpu.op.code_30,    "31": cpu.op.code_31,    "32": cpu.op.code_32,    "33": cpu.op.code_33,
    "34": cpu.op.code_34,    "35": cpu.op.code_35,    "36": cpu.op.code_36,    "37": cpu.op.code_37,
    "38": cpu.op.code_38,    "39": cpu.op.code_39,    "3a": cpu.op.code_3a,    "3b": cpu.op.code_3b,
    "3c": cpu.op.code_3c,    "3d": cpu.op.code_3d,    "3e": cpu.op.code_3e,    "3f": cpu.op.code_3f,

    "40": cpu.op.code_40,    "41": cpu.op.code_41,    "42": cpu.op.code_42,    "43": cpu.op.code_43,
    "44": cpu.op.code_44,    "45": cpu.op.code_45,    "46": cpu.op.code_46,    "47": cpu.op.code_47,
    "48": cpu.op.code_48,    "49": cpu.op.code_49,    "4a": cpu.op.code_4a,    "4b": cpu.op.code_4b,
    "4c": cpu.op.code_4c,    "4d": cpu.op.code_4d,    "4e": cpu.op.code_4e,    "4f": cpu.op.code_4f,

    "50": cpu.op.code_50,    "51": cpu.op.code_51,    "52": cpu.op.code_52,    "53": cpu.op.code_53,
    "54": cpu.op.code_54,    "55": cpu.op.code_55,    "56": cpu.op.code_56,    "57": cpu.op.code_57,
    "58": cpu.op.code_58,    "59": cpu.op.code_59,    "5a": cpu.op.code_5a,    "5b": cpu.op.code_5b,
    "5c": cpu.op.code_5c,    "5d": cpu.op.code_5d,    "5e": cpu.op.code_5e,    "5f": cpu.op.code_5f,

    "60": cpu.op.code_60,    "61": cpu.op.code_61,    "62": cpu.op.code_62,    "63": cpu.op.code_63,
    "64": cpu.op.code_64,    "65": cpu.op.code_65,    "66": cpu.op.code_66,    "67": cpu.op.code_67,
    "68": cpu.op.code_68,    "69": cpu.op.code_69,    "6a": cpu.op.code_6a,    "6b": cpu.op.code_6b,
    "6c": cpu.op.code_6c,    "6d": cpu.op.code_6d,    "6e": cpu.op.code_6e,    "6f": cpu.op.code_6f,

    "70": cpu.op.code_70,    "71": cpu.op.code_71,    "72": cpu.op.code_72,    "73": cpu.op.code_73,
    "74": cpu.op.code_74,    "75": cpu.op.code_75,    "76": cpu.op.code_76,    "77": cpu.op.code_77,
    "78": cpu.op.code_78,    "79": cpu.op.code_79,    "7a": cpu.op.code_7a,    "7b": cpu.op.code_7b,
    "7c": cpu.op.code_7c,    "7d": cpu.op.code_7d,    "7e": cpu.op.code_7e,    "7f": cpu.op.code_7f,
    
    "80": cpu.op.code_80,    "81": cpu.op.code_81,    "82": cpu.op.code_82,    "83": cpu.op.code_83,
    "84": cpu.op.code_84,    "85": cpu.op.code_85,    "86": cpu.op.code_86,    "87": cpu.op.code_87,
    "88": cpu.op.code_88,    "89": cpu.op.code_89,    "8a": cpu.op.code_8a,    "8b": cpu.op.code_8b,
    "8c": cpu.op.code_8c,    "8d": cpu.op.code_8d,    "8e": cpu.op.code_8e,    "8f": cpu.op.code_8f,

    "90": cpu.op.code_90,    "91": cpu.op.code_91,    "92": cpu.op.code_92,    "93": cpu.op.code_93,
    "94": cpu.op.code_94,    "95": cpu.op.code_95,    "96": cpu.op.code_96,    "97": cpu.op.code_97,
    "98": cpu.op.code_98,    "99": cpu.op.code_99,    "9a": cpu.op.code_9a,    "9b": cpu.op.code_9b,
    "9c": cpu.op.code_9c,    "9d": cpu.op.code_9d,    "9e": cpu.op.code_9e,    "9f": cpu.op.code_9f,

    "a0": cpu.op.code_a0,    "a1": cpu.op.code_a1,    "a2": cpu.op.code_a2,    "a3": cpu.op.code_a3,
    "a4": cpu.op.code_a4,    "a5": cpu.op.code_a5,    "a6": cpu.op.code_a6,    "a7": cpu.op.code_a7,
    "a8": cpu.op.code_a8,    "a9": cpu.op.code_a9,    "aa": cpu.op.code_aa,    "ab": cpu.op.code_ab,
    "ac": cpu.op.code_ac,    "ad": cpu.op.code_ad,    "ae": cpu.op.code_ae,    "af": cpu.op.code_af,

    "b0": cpu.op.code_b0,    "b1": cpu.op.code_b1,    "b2": cpu.op.code_b2,    "b3": cpu.op.code_b3,
    "b4": cpu.op.code_b4,    "b5": cpu.op.code_b5,    "b6": cpu.op.code_b6,    "b7": cpu.op.code_b7,
    "b8": cpu.op.code_b8,    "b9": cpu.op.code_b9,    "ba": cpu.op.code_ba,    "bb": cpu.op.code_bb,
    "bc": cpu.op.code_bc,    "bd": cpu.op.code_bd,    "be": cpu.op.code_be,    "bf": cpu.op.code_bf,

    "c0": cpu.op.code_c0,    "c1": cpu.op.code_c1,    "c2": cpu.op.code_c2,    "c3": cpu.op.code_c3,
    "c4": cpu.op.code_c4,    "c5": cpu.op.code_c5,    "c6": cpu.op.code_c6,    "c7": cpu.op.code_c7,
    "c8": cpu.op.code_c8,    "c9": cpu.op.code_c9,    "ca": cpu.op.code_ca,    "cb": cpu.op.code_cb,
    "cc": cpu.op.code_cc,    "cd": cpu.op.code_cd,    "ce": cpu.op.code_ce,    "cf": cpu.op.code_cf,

    "d0": cpu.op.code_d0,    "d1": cpu.op.code_d1,    "d2": cpu.op.code_d2,    "d3": cpu.op.code_d3,
    "d4": cpu.op.code_d4,    "d5": cpu.op.code_d5,    "d6": cpu.op.code_d6,    "d7": cpu.op.code_d7,
    "d8": cpu.op.code_d8,    "d9": cpu.op.code_d9,    "da": cpu.op.code_da,    "db": cpu.op.code_db,
    "dc": cpu.op.code_dc,    "dd": cpu.op.code_dd,    "de": cpu.op.code_de,    "df": cpu.op.code_df,

    "e0": cpu.op.code_e0,    "e1": cpu.op.code_e1,    "e2": cpu.op.code_e2,    "e3": cpu.op.code_e3,
    "e4": cpu.op.code_e4,    "e5": cpu.op.code_e5,    "e6": cpu.op.code_e6,    "e7": cpu.op.code_e7,
    "e8": cpu.op.code_e8,    "e9": cpu.op.code_e9,    "ea": cpu.op.code_ea,    "eb": cpu.op.code_eb,
    "ec": cpu.op.code_ec,    "ed": cpu.op.code_ed,    "ee": cpu.op.code_ee,    "ef": cpu.op.code_ef,

    "f0": cpu.op.code_f0,    "f1": cpu.op.code_f1,    "f2": cpu.op.code_f2,    "f3": cpu.op.code_f3,
    "f4": cpu.op.code_f4,    "f5": cpu.op.code_f5,    "f6": cpu.op.code_f6,    "f7": cpu.op.code_f7,
    "f8": cpu.op.code_f8,    "f9": cpu.op.code_f9,    "fa": cpu.op.code_fa,    "fb": cpu.op.code_fb,
    "fc": cpu.op.code_fc,    "fd": cpu.op.code_fd,    "fe": cpu.op.code_fe,    "ff": cpu.op.code_ff
}

op_cb_set = {
    "00": cpu.op.code_cb_00,    "01": cpu.op.code_cb_01,    "02": cpu.op.code_cb_02,    "03": cpu.op.code_cb_03,
    "04": cpu.op.code_cb_04,    "05": cpu.op.code_cb_05,    "06": cpu.op.code_cb_06,    "07": cpu.op.code_cb_07,
    "08": cpu.op.code_cb_08,    "09": cpu.op.code_cb_09,    "0a": cpu.op.code_cb_0a,    "0b": cpu.op.code_cb_0b,
    "0c": cpu.op.code_cb_0c,    "0d": cpu.op.code_cb_0d,    "0e": cpu.op.code_cb_0e,    "0f": cpu.op.code_cb_0f,

    "10": cpu.op.code_cb_10,    "11": cpu.op.code_cb_11,    "12": cpu.op.code_cb_12,    "13": cpu.op.code_cb_13,
    "14": cpu.op.code_cb_14,    "15": cpu.op.code_cb_15,    "16": cpu.op.code_cb_16,    "17": cpu.op.code_cb_17,
    "18": cpu.op.code_cb_18,    "19": cpu.op.code_cb_19,    "1a": cpu.op.code_cb_1a,    "1b": cpu.op.code_cb_1b,
    "1c": cpu.op.code_cb_1c,    "1d": cpu.op.code_cb_1d,    "1e": cpu.op.code_cb_1e,    "1f": cpu.op.code_cb_1f,

    "20": cpu.op.code_cb_20,    "21": cpu.op.code_cb_21,    "22": cpu.op.code_cb_22,    "23": cpu.op.code_cb_23,
    "24": cpu.op.code_cb_24,    "25": cpu.op.code_cb_25,    "26": cpu.op.code_cb_26,    "27": cpu.op.code_cb_27,
    "28": cpu.op.code_cb_28,    "29": cpu.op.code_cb_29,    "2a": cpu.op.code_cb_2a,    "2b": cpu.op.code_cb_2b,
    "2c": cpu.op.code_cb_2c,    "2d": cpu.op.code_cb_2d,    "2e": cpu.op.code_cb_2e,    "2f": cpu.op.code_cb_2f,

    "30": cpu.op.code_cb_30,    "31": cpu.op.code_cb_31,    "32": cpu.op.code_cb_32,    "33": cpu.op.code_cb_33,
    "34": cpu.op.code_cb_34,    "35": cpu.op.code_cb_35,    "36": cpu.op.code_cb_36,    "37": cpu.op.code_cb_37,
    "38": cpu.op.code_cb_38,    "39": cpu.op.code_cb_39,    "3a": cpu.op.code_cb_3a,    "3b": cpu.op.code_cb_3b,
    "3c": cpu.op.code_cb_3c,    "3d": cpu.op.code_cb_3d,    "3e": cpu.op.code_cb_3e,    "3f": cpu.op.code_cb_3f,

    "40": cpu.op.code_cb_40,    "41": cpu.op.code_cb_41,    "42": cpu.op.code_cb_42,    "43": cpu.op.code_cb_43,
    "44": cpu.op.code_cb_44,    "45": cpu.op.code_cb_45,    "46": cpu.op.code_cb_46,    "47": cpu.op.code_cb_47,
    "48": cpu.op.code_cb_48,    "49": cpu.op.code_cb_49,    "4a": cpu.op.code_cb_4a,    "4b": cpu.op.code_cb_4b,
    "4c": cpu.op.code_cb_4c,    "4d": cpu.op.code_cb_4d,    "4e": cpu.op.code_cb_4e,    "4f": cpu.op.code_cb_4f,

    "50": cpu.op.code_cb_50,    "51": cpu.op.code_cb_51,    "52": cpu.op.code_cb_52,    "53": cpu.op.code_cb_53,
    "54": cpu.op.code_cb_54,    "55": cpu.op.code_cb_55,    "56": cpu.op.code_cb_56,    "57": cpu.op.code_cb_57,
    "58": cpu.op.code_cb_58,    "59": cpu.op.code_cb_59,    "5a": cpu.op.code_cb_5a,    "5b": cpu.op.code_cb_5b,
    "5c": cpu.op.code_cb_5c,    "5d": cpu.op.code_cb_5d,    "5e": cpu.op.code_cb_5e,    "5f": cpu.op.code_cb_5f,

    "60": cpu.op.code_cb_60,    "61": cpu.op.code_cb_61,    "62": cpu.op.code_cb_62,    "63": cpu.op.code_cb_63,
    "64": cpu.op.code_cb_64,    "65": cpu.op.code_cb_65,    "66": cpu.op.code_cb_66,    "67": cpu.op.code_cb_67,
    "68": cpu.op.code_cb_68,    "69": cpu.op.code_cb_69,    "6a": cpu.op.code_cb_6a,    "6b": cpu.op.code_cb_6b,
    "6c": cpu.op.code_cb_6c,    "6d": cpu.op.code_cb_6d,    "6e": cpu.op.code_cb_6e,    "6f": cpu.op.code_cb_6f,

    "70": cpu.op.code_cb_70,    "71": cpu.op.code_cb_71,    "72": cpu.op.code_cb_72,    "73": cpu.op.code_cb_73,
    "74": cpu.op.code_cb_74,    "75": cpu.op.code_cb_75,    "76": cpu.op.code_cb_76,    "77": cpu.op.code_cb_77,
    "78": cpu.op.code_cb_78,    "79": cpu.op.code_cb_79,    "7a": cpu.op.code_cb_7a,    "7b": cpu.op.code_cb_7b,
    "7c": cpu.op.code_cb_7c,    "7d": cpu.op.code_cb_7d,    "7e": cpu.op.code_cb_7e,    "7f": cpu.op.code_cb_7f,

    "80": cpu.op.code_cb_80,    "81": cpu.op.code_cb_81,    "82": cpu.op.code_cb_82,    "83": cpu.op.code_cb_83,
    "84": cpu.op.code_cb_84,    "85": cpu.op.code_cb_85,    "86": cpu.op.code_cb_86,    "87": cpu.op.code_cb_87,
    "88": cpu.op.code_cb_88,    "89": cpu.op.code_cb_89,    "8a": cpu.op.code_cb_8a,    "8b": cpu.op.code_cb_8b,
    "8c": cpu.op.code_cb_8c,    "8d": cpu.op.code_cb_8d,    "8e": cpu.op.code_cb_8e,    "8f": cpu.op.code_cb_8f,

    "90": cpu.op.code_cb_90,    "91": cpu.op.code_cb_91,    "92": cpu.op.code_cb_92,    "93": cpu.op.code_cb_93,
    "94": cpu.op.code_cb_94,    "95": cpu.op.code_cb_95,    "96": cpu.op.code_cb_96,    "97": cpu.op.code_cb_97,
    "98": cpu.op.code_cb_98,    "99": cpu.op.code_cb_99,    "9a": cpu.op.code_cb_9a,    "9b": cpu.op.code_cb_9b,
    "9c": cpu.op.code_cb_9c,    "9d": cpu.op.code_cb_9d,    "9e": cpu.op.code_cb_9e,    "9f": cpu.op.code_cb_9f,

    "a0": cpu.op.code_cb_a0,    "a1": cpu.op.code_cb_a1,    "a2": cpu.op.code_cb_a2,    "a3": cpu.op.code_cb_a3,
    "a4": cpu.op.code_cb_a4,    "a5": cpu.op.code_cb_a5,    "a6": cpu.op.code_cb_a6,    "a7": cpu.op.code_cb_a7,
    "a8": cpu.op.code_cb_a8,    "a9": cpu.op.code_cb_a9,    "aa": cpu.op.code_cb_aa,    "ab": cpu.op.code_cb_ab,
    "ac": cpu.op.code_cb_ac,    "ad": cpu.op.code_cb_ad,    "ae": cpu.op.code_cb_ae,    "af": cpu.op.code_cb_af,

    "b0": cpu.op.code_cb_b0,    "b1": cpu.op.code_cb_b1,    "b2": cpu.op.code_cb_b2,    "b3": cpu.op.code_cb_b3,
    "b4": cpu.op.code_cb_b4,    "b5": cpu.op.code_cb_b5,    "b6": cpu.op.code_cb_b6,    "b7": cpu.op.code_cb_b7,
    "b8": cpu.op.code_cb_b8,    "b9": cpu.op.code_cb_b9,    "ba": cpu.op.code_cb_ba,    "bb": cpu.op.code_cb_bb,
    "bc": cpu.op.code_cb_bc,    "bd": cpu.op.code_cb_bd,    "be": cpu.op.code_cb_be,    "bf": cpu.op.code_cb_bf,

    "c0": cpu.op.code_cb_c0,    "c1": cpu.op.code_cb_c1,    "c2": cpu.op.code_cb_c2,    "c3": cpu.op.code_cb_c3,
    "c4": cpu.op.code_cb_c4,    "c5": cpu.op.code_cb_c5,    "c6": cpu.op.code_cb_c6,    "c7": cpu.op.code_cb_c7,
    "c8": cpu.op.code_cb_c8,    "c9": cpu.op.code_cb_c9,    "ca": cpu.op.code_cb_ca,    "cb": cpu.op.code_cb_cb,
    "cc": cpu.op.code_cb_cc,    "cd": cpu.op.code_cb_cd,    "ce": cpu.op.code_cb_ce,    "cf": cpu.op.code_cb_cf,

    "d0": cpu.op.code_cb_d0,    "d1": cpu.op.code_cb_d1,    "d2": cpu.op.code_cb_d2,    "d3": cpu.op.code_cb_d3,
    "d4": cpu.op.code_cb_d4,    "d5": cpu.op.code_cb_d5,    "d6": cpu.op.code_cb_d6,    "d7": cpu.op.code_cb_d7,
    "d8": cpu.op.code_cb_d8,    "d9": cpu.op.code_cb_d9,    "da": cpu.op.code_cb_da,    "db": cpu.op.code_cb_db,
    "dc": cpu.op.code_cb_dc,    "dd": cpu.op.code_cb_dd,    "de": cpu.op.code_cb_de,    "df": cpu.op.code_cb_df,

    "e0": cpu.op.code_cb_e0,    "e1": cpu.op.code_cb_e1,    "e2": cpu.op.code_cb_e2,    "e3": cpu.op.code_cb_e3,
    "e4": cpu.op.code_cb_e4,    "e5": cpu.op.code_cb_e5,    "e6": cpu.op.code_cb_e6,    "e7": cpu.op.code_cb_e7,
    "e8": cpu.op.code_cb_e8,    "e9": cpu.op.code_cb_e9,    "ea": cpu.op.code_cb_ea,    "eb": cpu.op.code_cb_eb,
    "ec": cpu.op.code_cb_ec,    "ed": cpu.op.code_cb_ed,    "ee": cpu.op.code_cb_ee,    "ef": cpu.op.code_cb_ef,

    "f0": cpu.op.code_cb_f0,    "f1": cpu.op.code_cb_f1,    "f2": cpu.op.code_cb_f2,    "f3": cpu.op.code_cb_f3,
    "f4": cpu.op.code_cb_f4,    "f5": cpu.op.code_cb_f5,    "f6": cpu.op.code_cb_f6,    "f7": cpu.op.code_cb_f7,
    "f8": cpu.op.code_cb_f8,    "f9": cpu.op.code_cb_f9,    "fa": cpu.op.code_cb_fa,    "fb": cpu.op.code_cb_fb,
    "fc": cpu.op.code_cb_fc,    "fd": cpu.op.code_cb_fd,    "fe": cpu.op.code_cb_fe,    "ff": cpu.op.code_cb_ff
}

if __name__ == '__main__':
    cpu = CPU()
