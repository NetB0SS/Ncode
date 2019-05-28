from backend.model.db import db


class Shfood(db.Model):
    __tablename__ = 'test9'
    ROWNUM_= db.Column(db.String(255), primary_key=True)
    FDDBR = db.Column(db.String(255))
    FZJG = db.Column(db.String(255))
    JYCSXXDZ = db.Column(db.String(255))
    JYXM = db.Column(db.String(255))
    QFR= db.Column(db.String(255))
    QFRQ = db.Column(db.Integer)
    QYMC_ZW = db.Column(db.String(255))
    RCJGJG =db.Column(db.String(255))
    RCJGRY =db.Column(db.String(255))
    SHXYDM =db.Column(db.String(255))
    XSFS =db.Column(db.String(255))
    XSLB =db.Column(db.String(255))
    ZSXXDZ =db.Column(db.String(255))
    ZTYTMXZW =db.Column(db.String(255))
    ZSID =db.Column(db.String(255))
    YXQZ =db.Column(db.String(255))
    ZSBH =db.Column(db.String(255))


    def __init__(self, ROWNUM_,FDDBR, FZJG, JYCSXXDZ, JYXM, QFR,QFRQ, QYMC_ZW,RCJGJG,RCJGRY,SHXYDM,XSFS,XSLB,ZSXXDZ,ZTYTMXZW,ZSID,YXQZ,ZSBH,index):

        self.ROWNUM_ = ROWNUM_
        self.FDDBR = FDDBR
        self.FZJG = FZJG
        self.JYCSXXDZ = JYCSXXDZ
        self.JYXM = JYXM
        self.QFR = QFR
        self.QFRQ = QFRQ
        self.QYMC_ZW = QYMC_ZW
        self.RCJGJG = RCJGJG
        self.RCJGRY = RCJGRY
        self.SHXYDM = SHXYDM
        self.XSFS = XSFS
        self.XSLB = XSLB
        self.ZSXXDZ = ZSXXDZ
        self.ZTYTMXZW = ZTYTMXZW
        self.ZSID = ZSID
        self.YXQZ = YXQZ
        self.ZSBH = ZSBH
