

class Ref:
    def __init__(self, obj):
        self.obj = obj
    
    @property
    def value(self):
        return {"Ref": self.obj.name}

class GetAtt:
    def __init__(self, obj, get_att:str):
        self.obj = obj
        self.get_att = get_att
    
    @property
    def value(self):
        return {"Fn::GetAtt": [self.obj.name, self.get_att]}

class AwsNoValue:
    value = {"Ref": "AWS::NoValue"}
