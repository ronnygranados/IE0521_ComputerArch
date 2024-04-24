empty = [] # lista vacia
pc_size = 3
local_size = 4
local_reg = ""


for i in range(local_size):
    local_reg += "0"
    
# print(local_reg)

empty = [local_reg for i in range(pc_size)]
entry_reg = empty[1]
entry_reg = entry_reg[-local_size+1:] + "1"

empty[1] = entry_reg
# print(entry_reg)
print(empty)