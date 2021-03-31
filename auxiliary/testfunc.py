
x = "awesome"

def myfunc():
    #print("Python is " + x)
    global x
    x= "gilipollas"

myfunc()
print(x)