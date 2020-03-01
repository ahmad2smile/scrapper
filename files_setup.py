

def appendToFile(name, data):
    with open(f"./data/{name}.txt", "a+", encoding="utf-8") as dataFile:
        dataFile.write(data)
