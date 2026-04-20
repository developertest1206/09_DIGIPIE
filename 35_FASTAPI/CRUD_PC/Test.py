def add(firstname : str | list[int], lastname : str):
    return firstname + " " + lastname

fname = "d"
lname = "gates"

name = add(fname, lname)
print(name)