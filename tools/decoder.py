class Decoder:
    def __init__(self):
        self.table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
        self.s = [11, 10, 3, 8, 4, 6]
        self.xor = 177451812
        self.add = 8728348608
        self.tr = {}
        
        for i in range(58):
            self.tr[self.table[i]]=i

    def get_bvnum(self, av_num):
        r = list('BV1  4 1 7  ')
        av_num = (av_num^self.xor) + self.add
        
        for i in range(6):
            r[self.s[i]] = self.table[av_num//58**i%58]
        
        bv_num = ''.join(r)
        
        return bv_num
