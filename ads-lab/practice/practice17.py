# q using stacks

st1 = []
st2 = []

def enq(val):
    st1.append(val)
    print(f"Inserted element {val} into q")

def process():
    if not st1:
        print("Queue empty.")
        return None
    res = []
    while st1:
        st2.append(st1.pop())
    while st2:
        res.append(st2.pop())
    return res
def deq():
    if not st1:
        print("Queue empty.")
        return None
    res = []
    while st1:
        st2.append(st1.pop())
    while st2:
        res.append(st2.pop())
    return res

enq(2)
enq(3)
enq(4)
enq(5)

print(deq())


