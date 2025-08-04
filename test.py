

def lala():
    ha = 5
    try:
        yield ha

    finally:
        print("carcthing///")

def test():
    iter = lala()

    ha = next(iter)
    print(ha)
    iter.close()
    
    print("This happens at very end of function")

test()

print("This happens at very end of program")
