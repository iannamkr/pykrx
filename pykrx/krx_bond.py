from pykrx.krx_http import MarketDataHttp
from pandas import DataFrame


class MKD40038(MarketDataHttp):
    # 지표 수익률 (20140303 ~ 현재)
    # - http://marketdata.krx.co.kr/mdi#document=05030403
    @property
    def bld(self):
        return "MKD/05/0503/05030403/mkd05030403"

    def scraping(self, fromdate, todate):
        try:
            result = self.post(fr_work_dt=fromdate, to_work_dt=todate)
            if len(result['block1']) == 0:
                return None

            df = DataFrame(result['block1'])
            df = df[['trd_dd', 'prc_yd1', 'prc_yd2', 'prc_yd3', 'prc_yd4', 'prc_yd5']]
            df.columns = ['일자', '3년물', '5년물', '10년물', '20년물', '30년물']
            df.set_index('일자', inplace=True)

            df.index = [x.replace('/', '-') for x in df.index]
            df = df.astype(float)
            df.index.name = "지표수익률"
            return df
        except (TypeError, IndexError, KeyError) as e:
            print(e)
            return None

class MKD40013(MarketDataHttp):
    # 장외 일자별 채권수익률
    # - http://marketdata.krx.co.kr/mdi#document=05030401
    @property
    def bld(self):
        return "MKD/05/0503/05030401/mkd05030401"

    def scraping(self, date):
        '''
        :param date:
        :return:
                            수익률    등락폭
            국고채 1년        1.743   -0.008
            국고채 3년        1.786   -0.015
            국고채 5년        1.853   -0.023
            국고채 10년       1.965   -0.030
            국고채 20년       2.039   -0.022
            국고채 30년       2.034   -0.021
        '''
        try:
            result = self.post(schdate=date)
            if len(result['block1']) == 0:
                return None

            df = DataFrame(result['block1'])
            df = df[['str_const_val', 'lst_ord_bas_yd', 'fluc_chgrng']]
            df.columns = ['채권종류', '수익률', '등락폭']
            df = df.astype({"수익률": float, "등락폭": float})
            df.set_index('채권종류', inplace=True)
            df.index.name = "장외 일자별 채권수익률"
            return df
        except (TypeError, IndexError, KeyError) as e:
            print(e)
            return None


if __name__ == "__main__":
    import pandas as pd
    pd.set_option('display.width', None)

    df = MKD40013().scraping("20190202")
    print(df)