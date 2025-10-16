class Storage():
    def __init__(self, code: dict = None):
        self.code = {}

        if code:
            self.code[code] = {}

    def addCode(self, code):
        codes = self.code.keys()

        if code not in codes:
            self.code[code] = {}
        else:
            pass 
    
    def addInfo(self, code, name, item, type_, price, names=[]):
        self.code[code]["name"] = name
        self.code[code]["item"] = item
        self.code[code]["type"] = type_
        self.code[code]["price"] = price
        self.code[code]["names"] = names
    
    def getInfo(self, code):
        return self.code[code] 
    
    def Addname(self, code, username):
        self.code[code]["names"].append(username)
