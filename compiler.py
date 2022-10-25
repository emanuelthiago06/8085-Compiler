import opcode
import regex__patterns
import values
import re
import somerandomfunction as srf

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
    

    def runner(self):
        self.get_text_values()
        self.get_labels()
        self.parse_op_code()
        self.generate_text()


    def generate_text(self):
        with open('compilacao_results.txt','w') as file:
            index = 0
            index2 = 0
            file.write("Posicao    op_code    linha\n")
            for i in self.op_code:
                for j in i[0]:
                    print(j)
                    file.write(f'{index}    {j}    {i[1]}\n')
                    index+=1


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
                    print(self.text)
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
    def get_labels(self):
        index = 0
        adress = 0
        self.label_adress = self.label.copy()
        for line in self.text:
            if not self.command[index]: 
                if self.command[index] not in values.commands:
                    raise SystemError(f"Comando inválido na linha {index}")
                    break
            else:
                if self.label:
                    self.label_adress.append(adress)
                    adress +=1
                adress += values.commands[self.command[index]]
            self.label_adress[index] = adress
            index+=1
    
    