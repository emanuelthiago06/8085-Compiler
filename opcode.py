from logging import raiseExceptions
import registers as regs
import somerandomfunction as srf
import values

def op_code_empty(opcode,arg1,arg2):
    if arg1 != " ":
        raise SystemError("Muitos argumentos")
    if arg2 != " ":
        raise SystemError("Muitos argumentos")
    return [opcode]

def op_code_reg(opcode,arg1,arg2):
    if arg2 != " ":
        raise SystemError("Muitos argumentos")
    if arg1 not in regs.registers:
        raise SystemError("Argumento inválido")
    else:
        return [opcode+regs.registers[arg1]];
def op_code_reg2(opcode,opcode2,arg1,arg2):
    if arg2 != " ":
        raise SystemError("Muitos argumentos")
    if arg1 not in regs.registers:
        raise SystemError("Argumento inválido")
    else:
        return [opcode+regs.registers[arg1]+opcode2];
def op_code_reg_lit(opcode,opcode2,arg1,arg2):
    if arg1 not in regs.registers:
        raise SystemError("Argumento inválido")
    return [opcode+regs.registers[arg1]+opcode2,srf.dec_to_bin(int(arg2)).zfill(8)]
def op_code_regs(opcode,arg1,arg2):
    if arg1 not in regs.registers:
        raise SystemError("Argumento inválido")
    return [opcode+regs.registers[arg1]+regs.registers[arg2]]
def op_code_lit(opcode,arg1,arg2):
    if arg2 != " ":
        raise SystemError("Muitos argumentos")
    temp = srf.dec_to_bin(int(arg1))
    if srf.is_number(arg1):
        raise SystemError("Argumento inválido, somente números")
    return [opcode,temp.zfill(8)]

def op_code_lit2(opcode1,opcode2,arg1,arg2):
    if arg1 not in regs.registers:
        raise SystemError("Argumento inválido")
    if arg2 != " ":
        raise SystemError("Muitos argumentos")
    return [opcode1 + regs.registers[arg1] + opcode2]

def op_code_big(opcode,arg1,arg2):
    if arg2 != " ":
        raise SystemError("Muitos argumentos")
    if arg1 not in values.commands:
        raise SystemError("Argumento inválido") 
    temp = srf.dec_to_bin(int(arg1)).zfill(16)
    return [opcode, temp[8:16], temp[0:8]]

def op_code_big_alt(opcode,arg1,arg2,text,alt):
    if arg2 != " ":
        raise SystemError("Muitos argumentos")
    index = 0
    if arg1 in text: 
        for label in text:
            if arg1 == label:
                print(alt[index])
                temp = srf.dec_to_bin(alt[index]).zfill(16)
            index+=1
    else:
        if arg1 not in values.commands:
            raise SystemError("Argumento inválido") 
        else:
            temp = srf.dec_to_bin(int(arg1)).zfill(16)
    return [opcode, temp[8:16],temp[0:8]]
    
def opcode_special(opcode1, opcode2,arg1,arg2):
    if arg2 is not None:
        raise SyntaxError('Argumento inválido')

    if arg1 not in ['d', 'b']:
        raise SyntaxError('Argumento inválido')
    temp = 0
    if arg1 == 'b':
        temp = '0'
    else:
        temp = '1' 

    return [opcode1 + temp + opcode2]
def opcode_special2(opcode1, opcode2,arg1,arg2):
    if arg2 != " ":
        raise SystemError("Muitos argumentos")
    if arg1 not in regs.registers:
        raise SyntaxError('Argumento inválido')

    return [opcode1 + regs.registers[arg1] + opcode2]

def opcode_special2_double(opcode1, opcode2,arg1,arg2):
    if arg2 != " ":
        raise SystemError("Muitos argumentos")
    temp = srf.dec_to_bin(int(arg1)).zfill(16)
    if arg1 not in regs.registers:
        raise SyntaxError('Argumento inválido')
    return [opcode1 + regs.registers[arg1] + opcode2, temp[8:16], temp[0:8]]
def db_treat(arg1):
    temp = srf.dec_to_bin(int(arg1)).zfill(8)
    if len(temp)>8:
        raise SyntaxError("Estouro")
    return [temp]
def ds_treat(arg1):
    temp = []
    print(type(arg1))
    for i in range(int(arg1)):
        temp.append("00000000")
    return temp
def treat_org(arg1,texto,ad):
    return ["00000000"]

op_code_table = {
    'adc': lambda arg1,arg2,text,ad: op_code_reg('10001', arg1,arg2),
    'aci': lambda arg1,arg2,text,ad: op_code_lit('11001110', arg1,arg2),
    'add': lambda arg1,arg2,text,ad: op_code_reg('10000', arg1,arg2),
    'adi': lambda arg1,arg2,text,ad: op_code_lit('11000110', arg1,arg2),
    'ana': lambda arg1,arg2,text,ad: op_code_reg('10100', arg1,arg2),
    'ani': lambda arg1,arg2,text,ad: op_code_lit('11100110', arg1,arg2),
    'call': lambda arg1,arg2,text,ad: op_code_big('11001101', arg1,arg2),
    'cc': lambda arg1,arg2,text,ad:op_code_big('11011100', arg1,arg2),
    'cm': lambda arg1,arg2,text,ad:op_code_big('11111100', arg1,arg2),
    'cmc': lambda arg1,arg2,text,ad: op_code_empty('00111111', arg1,arg2),
    'cma': lambda arg1,arg2,text,ad: op_code_empty('00101111', arg1,arg2),
    'cmp': lambda arg1,arg2,text,ad: op_code_reg('10111', arg1,arg2),
    'cnc': lambda arg1,arg2,text,ad: op_code_big('11010100', arg1,arg2),
    'cnz': lambda arg1,arg2,text,ad: op_code_big('11000100', arg1,arg2),
    'cp': lambda arg1,arg2,text,ad:op_code_big('11110100', arg1,arg2),
    'cpe': lambda arg1,arg2,text,ad: op_code_big('11101100', arg1,arg2),
    'cpi': lambda arg1,arg2,text,ad: op_code_lit('11111110', arg1,arg2),
    'cpo': lambda arg1,arg2,text,ad: op_code_big('11100100', arg1,arg2),
    'cz': lambda arg1,arg2,text,ad:op_code_big('11001100',arg1,arg2),
    'daa': lambda arg1,arg2,text,ad: op_code_empty('00100111',arg1,arg2),
    'dad': lambda arg1,arg2,text,ad: opcode_special2('00', '1001',arg1,arg2),
    'dcr': lambda arg1,arg2,text,ad: op_code_lit2('00', '101',arg1,arg2),
    'dcx': lambda arg1,arg2,text,ad: opcode_special2('00', '1011', arg1,arg2),
    'ei': lambda arg1,arg2,text,ad:op_code_empty('11111011', arg1,arg2),
    'di': lambda arg1,arg2,text,ad:op_code_empty('11110011', arg1,arg2),
    'hlt': lambda arg1,arg2,text,ad: op_code_empty('01110110', arg1,arg2),
    'in': lambda arg1,arg2,text,ad:op_code_lit('11011011', arg1,arg2),
    'inr': lambda arg1,arg2,text,ad: op_code_lit2('00', '100', arg1,arg2),
    'inx': lambda arg1,arg2,text,ad: opcode_special2('00', '0011', arg1,arg2),
    'jc': lambda arg1,arg2,text,ad:op_code_big_alt('11011010', arg1,arg2,text,ad),
    'jm': lambda arg1,arg2,text,ad:op_code_big_alt('11111010', arg1,arg2,text,ad),
    'jmp': lambda arg1,arg2,text,ad: op_code_big_alt('11000011', arg1,arg2,text,ad),
    'jnc': lambda arg1,arg2,text,ad: op_code_big_alt('11010010', arg1,arg2,text,ad),
    'jnz': lambda arg1,arg2,text,ad: op_code_big_alt('11000010', arg1,arg2,text,ad),
    'jp': lambda arg1,arg2,text,ad:op_code_big_alt('11110010', arg1,arg2,text,ad),
    'jpe': lambda arg1,arg2,text,ad: op_code_big_alt('11101010', arg1,arg2,text,ad),
    'jpo': lambda arg1,arg2,text,ad: op_code_big_alt('11100010', arg1,arg2,text,ad),
    'jz': lambda arg1,arg2,text,ad:op_code_big_alt('11001010', arg1,arg2,text,ad),
    'lda': lambda arg1,arg2,text,ad: op_code_big('00111010', arg1,arg2),
    'ldax': lambda arg1,arg2,text,ad: opcode_special('000', '1010', arg1,arg2),
    'lhld': lambda arg1,arg2,text,ad: op_code_big('00101010', arg1,arg2),
    'lxi': lambda arg1,arg2,text,ad: opcode_special2_double('00', '0001',arg1,arg2),
    'mov': lambda arg1,arg2,text,ad: op_code_regs('01',arg1,arg2),
    'mvi': lambda arg1,arg2,text,ad: op_code_reg_lit('00', '110',arg1,arg2),
    'nop': lambda arg1,arg2,text,ad: op_code_empty('00000000', arg1,arg2),
    'ora': lambda arg1,arg2,text,ad: op_code_reg('10110',arg1,arg2),
    'ori': lambda arg1,arg2,text,ad: op_code_lit('11110110', arg1,arg2),
    'out': lambda arg1,arg2,text,ad: op_code_lit('11010011', arg1,arg2),
    'pchl': lambda arg1,arg2,text,ad: op_code_empty('11101001', arg1,arg2),
    'pop': lambda arg1,arg2,text,ad: opcode_special2('11', '0001', arg1,arg2),
    'push': lambda arg1,arg2,text,ad: opcode_special2('11', '0101', arg1,arg2),
    'ral': lambda arg1,arg2,text,ad: op_code_empty('00010111', arg1,arg2),
    'rar': lambda arg1,arg2,text,ad: op_code_empty('00011111', arg1,arg2),
    'rc': lambda arg1,arg2,text,ad:op_code_empty('01010101', arg1,arg2),
    'ret': lambda arg1,arg2,text,ad: op_code_empty('11001001', arg1,arg2),
    'rim': lambda arg1,arg2,text,ad: op_code_empty('00100000', arg1,arg2),
    'rlc': lambda arg1,arg2,text,ad: op_code_empty('00000111', arg1,arg2),
    'rm': lambda arg1,arg2,text,ad:op_code_empty('11111000', arg1,arg2),
    'rnc': lambda arg1,arg2,text,ad: op_code_empty('11010000',arg1,arg2),
    'rnz': lambda arg1,arg2,text,ad: op_code_empty('11000000', arg1,arg2),
    'rp': lambda arg1,arg2,text,ad:op_code_empty('11110000', arg1,arg2),
    'rpe': lambda arg1,arg2,text,ad: op_code_empty('11101000', arg1,arg2),
    'rpo': lambda arg1,arg2,text,ad: op_code_empty('11100000', arg1,arg2),
    'rrc': lambda arg1,arg2,text,ad: op_code_empty('00001111', arg1,arg2),
    'rst': lambda arg1,arg2,text,ad: op_code_lit2('11', '111', arg1,arg2),
    'rz': lambda arg1,arg2,text,ad:op_code_empty('11001000', arg1,arg2),
    'sbb': lambda arg1,arg2,text,ad: op_code_reg('10011',arg1,arg2),
    'sbi': lambda arg1,arg2,text,ad: op_code_lit('11011110', arg1,arg2),
    'shld': lambda arg1,arg2,text,ad: op_code_big('00100010', arg1,arg2),
    'sim': lambda arg1,arg2,text,ad: op_code_empty('00110000', arg1,arg2),
    'sphl': lambda arg1,arg2,text,ad: op_code_empty('11111001', arg1,arg2),
    'sta': lambda arg1,arg2,text,ad: op_code_big('00110010', arg1,arg2),
    'stax': lambda arg1,arg2,text,ad: opcode_special('000', '0010', arg1,arg2),
    'stc': lambda arg1,arg2,text,ad: op_code_empty('00110111', arg1,arg2),
    'sub': lambda arg1,arg2,text,ad: op_code_reg('10010', arg1,arg2),
    'sui': lambda arg1,arg2,text,ad: op_code_lit('11010110', arg1,arg2),
    'xchg': lambda arg1,arg2,text,ad: op_code_empty('11101011', arg1,arg2),
    'xra': lambda arg1,arg2,text,ad: op_code_reg('10101', arg1,arg2),
    'xri': lambda arg1,arg2,text,ad: op_code_reg('11101110', arg1,arg2),
    'xthl': lambda arg1,arg2,text,ad: op_code_empty('11100011', arg1,arg2),
    'db': lambda arg1,arg2,text,ad: db_treat(arg1),
    'ds': lambda arg1,arg2,text,ad: ds_treat(arg1),
    'org': lambda arg1,arg2,text,ad: treat_org(arg1,arg2,text),
    'equ': lambda arg1,arg2,text,ad: [""]
}