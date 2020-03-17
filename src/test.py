from arkOperator import Arknights
if __name__ == "__main__":
    ark = Arknights()
    with open(r"userconfig.txt", mode='r') as file:
        for order in file.readlines():
            order = order.replace("\\","\\\\")
            exec(order,{'ark': ark})
    with open(r"singleOrders\\code.txt", mode='r') as file:
        for order in file.readlines():
            exec(order,{'ark': ark})
