# finish the function
def find_the_parent(child):
    parent = ''
    if issubclass(child, Drinks):
        parent = Drinks.__name__
    elif issubclass(child, Pastry):
        parent = Pastry.__name__
    elif issubclass(child, Sweets):
        parent = Sweets.__name__
    print(parent)
