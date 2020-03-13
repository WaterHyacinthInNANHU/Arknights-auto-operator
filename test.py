from arkOperator import Arknights
if __name__ == "__main__":
    ark = Arknights()
    file = open(r"code.txt",mode='r')
    for order in file.readlines():
        exec(order,{'ark': ark})
