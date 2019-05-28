from flask_restful import Resource,reqparse,abort,Api
from backend.model.shFood import Shfood
from backend.model.foodkey import Foodkey
import time


class Hello(Resource):
    def __init__(self):
        super(Hello, self).__init__()
        self.parser = reqparse.RequestParser()

    def get(self):

        return 'hello'



class Searchlicence(Resource):
    def __init__(self):
        super(Searchlicence, self).__init__()
        self.parser = reqparse.RequestParser()

    def post(self):
        self.parser.add_argument('address', type=str)
        args = self.parser.parse_args()
        addre=args['address']
        address = '%' + addre + '%'
        businessscope = Shfood.query.filter(Shfood.JYCSXXDZ.like(address)).all()
        if len (businessscope)>1:
            return {"status":"多条数据"}
        else:
            try:
                businessscope=businessscope[0]
                result=businessscope.YXQZ
                timeStamp = int(''.join(result)[:-3])
                timeArray = time.localtime(timeStamp)
                otherStyleTime = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)
                return {"经营范围": businessscope.JYXM,"发证机关":businessscope.FZJG,"有效期至":otherStyleTime,"所属机关":businessscope.RCJGJG,"证书编号":businessscope.ZSBH,"经营场所线下地址":businessscope.JYCSXXDZ}
            except AttributeError:
                return {"status":"GG"}



class Takekey(Resource):
    def __init__(self):
        super(Takekey, self).__init__()
        self.parser = reqparse.RequestParser()
    def post(self):
        self.parser.add_argument('type', type=str)
        args = self.parser.parse_args()
        businessscope = Foodkey.query.filter_by(e_type=args['type']).all()
        resultlist=[]
        if len(businessscope)>1:
            for each in businessscope:
                resultlist.append(each.name)
        return {'keylist':resultlist}

