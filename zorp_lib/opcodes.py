REGISTERS_8BIT  = [*"BCDEHL", "HLP", "A"]
REGISTERS_16BIT = ["BC", "DE", "HL", "SP"]

# shorthand versions of the opcodes to make patches easier to read/write
SHORTHANDS  = set()

MISC_OPCODES = dict(
    NOP  = 0x00,
    STOP = 0x10,
    HALT = 0x76,

    DI   = 0xF3,
    EI   = 0xFB,
    )

BITWISE_OPCODES_8BIT = dict(
    RLCA = 0x07,
    RRCA = 0x0F,
    RLA  = 0x17,
    RRA  = 0x1F,
    )


BITWISE_OPCODES_8BIT_EXT = dict()
for i, op in enumerate([
         "RLC", "RRC",   "RL",  "RR",
         "SLA", "SRA", "SWAP", "SRL",
        *(f"BIT{n}" for n in range(8)),
        *(f"RES{n}" for n in range(8)),
        *(f"SET{n}" for n in range(8)),
        ]):
    BITWISE_OPCODES_8BIT_EXT.update({
        f'{op}_{r}': b'\xCB' + bytes([i*0x8 | j])
        for j, r in enumerate(REGISTERS_8BIT)
        })


MATH_OPCODES_8BIT = dict(
    ADD     = 0xC6,
    ADC     = 0xCE,
    SUB     = 0xD6,
    SBC     = 0xDE,
    AND     = 0xE6,
    XOR     = 0xEE,
    OR      = 0xF6,
    CP      = 0xFE,
    )
LOAD_OPCODES_8BIT = dict(
    LD_B    = 0x06,
    LD_C    = 0x0E,
    LD_D    = 0x16,
    LD_E    = 0x1E,
    LD_H    = 0x26,
    LD_L    = 0x2E,
    LD_HLP  = 0x36,
    LD_A    = 0x3E,
    )
LOAD_OPCODES_16BIT = dict(
    LD_BC   = 0x01,
    LD_DE   = 0x11,
    LD_HL   = 0x21,
    LD_SP   = 0x31,
    )

for k, v in tuple(MATH_OPCODES_8BIT.items()):
    MATH_OPCODES_8BIT[f"{k}_D8"] = v
    SHORTHANDS.add(k)

for k, v in tuple(LOAD_OPCODES_8BIT.items()):
    LOAD_OPCODES_8BIT[f"{k}_D8"] = v
    SHORTHANDS.add(k)

for k, v in tuple(LOAD_OPCODES_16BIT.items()):
    LOAD_OPCODES_16BIT[f"{k}_D16"] = v
    SHORTHANDS.add(k)


MATH_OPCODES_8BIT.update(
    DAA = 0x27,
    SCF = 0x37,
    CPL = 0x2F,
    CCF = 0x3F,
    )
LOAD_OPCODES_8BIT.update(
    LD_BCP_A    = 0x02,
    LD_A_BCP    = 0x0A,
    LD_DEP_A    = 0x12,
    LD_A_DEP    = 0x1A,
    LDI_HLP_A   = 0x22,
    LDI_A_HLP   = 0x2A,
    LDD_HLP_A   = 0x32,
    LDD_A_HLP   = 0x3A,

    LD_A16_A    = 0xEA,
    LD_A_A16    = 0xFA,
    LDH_A8_A    = 0xE0,
    LDH_A_A8    = 0xF0,

    LD_CP_A     = 0xE2,
    LD_A_CP     = 0xF2,
    )
LOAD_OPCODES_16BIT.update(
    LD_A16_SP   = 0x08,

    POP_BC      = 0xC1,
    POP_DE      = 0xD1,
    POP_HL      = 0xE1,
    POP_AF      = 0xF1,

    PUSH_BC     = 0xC5,
    PUSH_DE     = 0xD5,
    PUSH_HL     = 0xE5,
    PUSH_AF     = 0xF5,

    LD_HL_SP_R8 = 0xF8,
    LD_SP_HL    = 0xF9,
    ADD_SP_R8   = 0xE8,
    )

for i, r in enumerate(REGISTERS_8BIT):
    LOAD_OPCODES_8BIT.update({
        f"LD_B_{r}":   0x40|i,
        f"LD_C_{r}":   0x48|i,
        f"LD_D_{r}":   0x50|i,
        f"LD_E_{r}":   0x58|i,
        f"LD_H_{r}":   0x60|i,
        f"LD_L_{r}":   0x68|i,
        f"LD_HLP_{r}": 0x70|i,
        f"LD_A_{r}":   0x78|i,
        })

# doesn't exist
del LOAD_OPCODES_8BIT["LD_HLP_HLP"]


for i, r in enumerate(REGISTERS_8BIT):
    MATH_OPCODES_8BIT.update({
        f"INC_{r}": 0x04+(0x08*i),
        f"DEC_{r}": 0x05+(0x08*i),

        f"ADD_{r}": 0x80|i,
        f"ADC_{r}": 0x88|i,
        f"SUB_{r}": 0x90|i,
        f"SBC_{r}": 0x98|i,
        f"AND_{r}": 0xA0|i,
        f"XOR_{r}": 0xA8|i,
        f"OR_{r}":  0xB0|i,
        f"CP_{r}":  0xB8|i,
        })

MATH_OPCODES_16BIT = {}
for i, r in enumerate(REGISTERS_16BIT):
    MATH_OPCODES_16BIT.update({
        f"INC_{r}":     0x03+(0x10*i),
        f"DEC_{r}":     0x0B+(0x10*i),
        f"ADD_HL_{r}":  0x09+(0x10*i),
        })


JUMP_OPCODES = dict(
    JR    = 0x18,
    JR_NZ = 0x20,
    JR_Z  = 0x28,
    JR_NC = 0x30,
    JR_C  = 0x38,

    RET    = 0xC9,
    RET_I  = 0xD9,
    RET_NZ = 0xC0,
    RET_Z  = 0xC8,
    RET_NC = 0xD0,
    RET_C  = 0xD8,

    CALL    = 0xCD,
    CALL_NZ = 0xC4,
    CALL_Z  = 0xCC,
    CALL_NC = 0xD4,
    CALL_C  = 0xDC,

    JP     = 0xC3,
    JP_HLP = 0xE9,
    JP_NZ  = 0xC2,
    JP_Z   = 0xCA,
    JP_NC  = 0xD2,
    JP_C   = 0xDA,

    **{f"RST_{v}H": 0xC7+(0x08*i)
       for i, v in enumerate(["00", "08", "10", "18",
                              "20", "28", "30", "38"])
       }
    )

REPLACE_MAP = {
    **LOAD_OPCODES_8BIT,
    **LOAD_OPCODES_16BIT,
    **MATH_OPCODES_8BIT,
    **MATH_OPCODES_16BIT,
    **BITWISE_OPCODES_8BIT,
    **BITWISE_OPCODES_8BIT_EXT,
    **MISC_OPCODES,
    **JUMP_OPCODES,
    }

globals().update({name: name for name in set([
    *LOAD_OPCODES_8BIT, *LOAD_OPCODES_16BIT,
    *MATH_OPCODES_8BIT, *MATH_OPCODES_16BIT,
    *BITWISE_OPCODES_8BIT, *BITWISE_OPCODES_8BIT_EXT,
    *MISC_OPCODES, *JUMP_OPCODES,
    ])})

def print_opcode_tables():
    '''
    Prints a table of all opcodes in the same format as the URL below:
        https://www.pastraiser.com/cpu/gameboy/gameboy_opcodes.html
    For debugging purposes.
    '''
    table1 = [""] * 256
    table2 = [""] * 256
    max_len = 0
    for name, index in dict(
            **LOAD_OPCODES_8BIT, **LOAD_OPCODES_16BIT,
            **MATH_OPCODES_8BIT, **MATH_OPCODES_16BIT,
            **BITWISE_OPCODES_8BIT, **MISC_OPCODES, **JUMP_OPCODES,
            ).items():
        if name not in SHORTHANDS:
            table1[index] = name
            max_len = max(len(name), max_len)

    for name, index in BITWISE_OPCODES_8BIT_EXT.items():
        table2[index[1]] = name
        max_len = max(len(name), max_len)

    head_top  = list(f"0x0{i}" for i in "0123456789ABCDEF")
    head_side = list(f"0x{i}0" for i in "0123456789ABCDEF")
    head_side.insert(0, "")

    table1 = head_top + table1
    table2 = head_top + table2
    for i in range(len(table1)-0x10, -1, -0x10):
        char = head_side.pop()
        table1.insert(i, char)
        table2.insert(i, char)

    max_len += 2 # add padding to both sides
    row_str = "+".join("-" * (max_len-1) for _ in range(0x11))
    row_str = f"+{row_str}+"

    for table, name in (
            [table1, "Standard instruction set"],
            [table2, "Extended instruction set(Prefix 0xCB)"],
            ):
        print("\n", name, sep="")
        print(row_str)
        for i in range(0, len(table), 0x11):
            for c in table[i:i+0x11]:
                padl = " "*((max_len - len(c)-1)//2)
                padr = " "*((max_len - len(c)  )//2)
                print("|", padl, c, padr, sep="", end="")

            print("|")
            print(row_str)

JR_OPCODES = set([
    JR,
    JR_NZ,
    JR_Z,
    JR_NC,
    JR_C,
    ])

class Label(str):
    pass

if __name__ == "__main__":
    print_opcode_tables()
    input()
