from atexit import register
import opcode
import regex__patterns
import values
import re
import somerandomfunction as srf
from ast import literal_eval
import registers
from add_types_support import *
#import pandas as pd

class Comp8085:
    def __init__(self,path):
        self.path = path
        self.text = []
        self.command = []
        self.label = []
        self.label_adress = []
        self.arg1 = []
        self.arg2 = []
        self.adress_def = []
        self.op_code = []
        self.glob = {}
    

    def runner(self):
        self.get_text_values()
        self.translate_args()
        self.get_labels()
        self.parse_op_code()
        print(self.op_code)
        self.generate_text()


    def generate_text(self):
        st1 = "posicao"
        st2 = "op_code"
        st3 = "linha"
        colums =  [st1,st2,st3]
        with open('compilacao_results.txt','w') as file:
            index = 0
            index2 = 0
            count = 0
            dicti = {}
            file.write(f"{st1:7}      op_code{st1:7}       linha{st1:7}\n")
            for i in self.op_code:
                for j in i[0]:
                    if index == 0:
                        dicti.update({(0+count): [j,i[1]]}) 
                    else:    
                        dicti.update({(self.label_adress[index2-1]+count) : [j,i[1]]})                
                    index+=1
                    count+=1
                #print(dicti)
                count = 0
                index2+=1
            for key,values in dicti.items():

                file.write(f'{key:7}       {values[0]:7}       {values[1]:7}\n')

    def get_text_values(self):
        count = 0
        flag = 0
        with open(self.path+'.txt', 'r') as file:
            for number, line in enumerate(file, start=1):
                line = line.lower()
                for pattern in regex__patterns.patterns:
                    if re.match(pattern, line):
                        self.text.append(line)
                        match2 = re.search(pattern,line)
                        if count == 0:
                            self.command.append(match2.group("command"))
                            self.label.append(" ")
                            self.arg1.append(" ")
                            self.arg2.append(" ")
                        if count == 1:
                            self.command.append(match2.group("command"))
                            self.label.append(" ")
                            self.arg1.append(match2.group("arg1"))
                            self.arg2.append(" ")
                        if count == 2:
                            self.command.append(match2.group("command"))
                            self.label.append(" ")
                            self.arg1.append(match2.group("arg1"))
                            self.arg2.append(match2.group("arg2"))
                        if count == 3:
                            self.command.append(match2.group("command"))
                            self.label.append(match2.group("label"))
                            self.arg1.append(match2.group("arg1"))
                            self.arg2.append(match2.group("arg2"))
                        if count == 4:
                            self.command.append(match2.group("command"))
                            self.label.append(match2.group("label"))
                            self.arg1.append(match2.group("arg1"))
                            self.arg2.append(" ")
                        if count == 5:
                            self.command.append(match2.group("command"))
                            self.label.append(match2.group("label"))
                            self.arg1.append(" ")
                            self.arg2.append(" ")
                        if count == 6:
                            self.command.append(" ")
                            self.label.append(" ")
                            self.arg1.append(" ")
                            self.arg2.append(" ")
                        flag+=1
                        break
                    count +=1       
                if flag == 0:
                    raise SyntaxError(f"Sintaxe inválida na linha {number}")
                count = 0
                flag = 0
    def parse_op_code(self):
        index = 0
        for line in self.text:
            if self.command[index]:
                ad_cmd = opcode.op_code_table[self.command[index]](self.arg1[index],self.arg2[index],self.label,self.label_adress)
            else:
                ad_cmd = ['00000000']
            index+=1
            self.op_code.append([ad_cmd,index])
    def translate_args(self):
        count = 0
        for i in self.arg1: 
            if is_oct(self.arg1[count]):
                self.arg1[count] = oct_to_dec(is_oct(self.arg1[count]))
            if is_bin(self.arg1[count]):
                self.arg1[count] = bin_to_dec(is_bin(self.arg1[count]))
            if is_hex(self.arg1[count]):
                self.arg1[count] = hex_to_dec(is_hex(self.arg1[count]))
            count+=1


    def get_labels(self):
        index = 0
        adress = 0
        count4 = 0
        self.label_adress = self.label.copy()
        for line in self.text: 
            if self.command[index] not in values.commands:
                    raise SystemError(f"Comando inválido na linha {index}")
                    break
            else:
                if self.command[index]:
                    if self.arg1[index] in self.glob:
                        self.arg1[index] = self.glob[self.arg1[index]]
                    if self.arg2[index] in self.glob:
                        self.arg2[index] = self.glob[self.arg2[index]]                    
                    if self.command[index] == "org":
                        if srf.is_number(self.arg1[index]):
                            if int(self.arg1[index]) >= 256*256:
                                raise SystemError("ESTOURO DE MEMÓRIA NO ORG")
                            adress = int(self.arg1[index])
                        elif self.arg1[index] in self.label[:index]:
                            count4 = 0
                            for i in self.label[:index]:
                                if self.arg1[index] == i:
                                    break
                                count4+=1
                            if count4 == 0:
                                adress += 1
                            else:
                                adress += self.label_adress[count4-1]+1
                    if self.command[index] == "ds":
                        if not srf.is_number(self.arg1[index]):
                            raise SystemError("o argumento do DS deve ser um número")
                        adress+= int(self.arg1[index])
                    if self.command[index] == 'equ':
                        if self.label[index] in self.label[:index]or self.label[index] == " " or self.label[index] in values.commands or self.label[index] in registers.registers or self.label[index] in registers.double_registers:
                            raise SystemError("label não pode ser vazia, não pode ser de uma variável reservada, ou redeclarada ")
                        self.glob.update({self.label[index]:self.arg1[index]})

                    adress += values.commands[self.command[index]]

                else:
                    if self.label[index]:
                        adress +=1
            self.label_adress[index] = adress
            index+=1
    
    