from ast import literal_eval

def fill_zeros(data,size):
    zero_list = []
    count = 0
    if len(data) >= size:
        return data;
    for it in range(size):
        zero_list.append('0')
    for it2 in data:
        zero_list[count] = str(int(data[count])+int(zero_list[count]))
        count+=1
    zero_list.reverse()
    return zero_list
def dec_to_bin(n):
    return bin(n).replace("0b", "")
def is_number(testable):
    print(testable)
    temp = literal_eval(testable)
    if isinstance(temp,int) or isinstance(temp,float):
        return True
    return False 
