from bs4 import BeautifulSoup
import requests

from data import StockDataMonthRevenue, StockDataYearRevenue


class StockDataSourcePcHome(object):

    def __init__(self):
        self.url = {
            "revenue":   "https://pchome.megatime.com.tw/stock/sto3/ock2/{}/sid{}.html",
            "financial": "https://pchome.megatime.com.tw/stock/sto2/ock2/{}{}/sid{}.html",
        }

    def get_revenue(self, stock_id: int, year: int):
        response = requests.post(self.url["revenue"].format(year, stock_id), data={"is_check": "1"})

        soup = BeautifulSoup(response.text, 'html.parser')

        month_th = soup.find("th", text="月份")
        assert month_th is not None

        th_tr = month_th.find_parent("tr")
        assert th_tr is not None
        assert [th.text for th in th_tr.find_all("th")] == \
               ["月份", "單月營收", "年成長率", "累計營收", "累計營收年成長率", "月份", "單月營收", "累計營收  ", "累計營收年成長率"]

        trs = [tr for tr in th_tr.find_next_siblings()]
        revenues = tuple()
        assert len(trs) == 12
        for i, tr in enumerate(trs):
            month, revenue = get_month_revenue(tr)
            if month is None:
                break
            assert month == (i + 1)

            revenues += (revenue, )
        return revenues

    def get_financial(self, stock_id: int, year: int, quarter: int):
        expect_leading_col = {
            0: "獲利能力",
            14: "經營績效",
            18: "償債能力",
            22: "經營能力",
            27: "資本結構",
        }
        financial_key_grade = {
            # 獲利能力
            "營業毛利率": "gross_margin",
            "營業利益率": "operating_profit_margin",
            "稅前淨利率": "net_income_margin",
            "稅後淨利率": "net_profit_margin",
            "每股淨值(C)": "net_worth_per_share",
            "每股營業額(元)": "revenue_per_share",
            "每股營業利益(元)": "operating_profit_per_share",
            "每股負債(元)": "debt_per_share",
            "每股現金流量(元)": "cash_flow_per_share",
            "每股稅前淨利(元)": "net_income_per_share",
            "每股稅後淨利(元)": "net_profit_per_share",
            "稅前淨值報酬率": "pre_tax_roe",
            "稅後淨值報酬率": "roe",
            "總資產報酬率": "roa",
            # 經營績效
            "營收成長率": "revenue_growth_rate",
            "營益成長率": "operating_profit_growth_rate",
            "稅前淨利成長率": "net_income_growth_rate",
            "固定資產成長率": "asset_growth_rate",
            # 償債能力
            "流動比率": "current_ratio",
            "速動比率": "quick_ratio",
            "負債比率": "debt_ratio",
            "應收帳款週轉率": "receivables_turnover_ratio",
            # 經營能力
            "存貨週轉率": "inventory_turnover_ratio",
            "固定資產週轉率": "asset_turnover_ratio",
            "每人營業額(仟元)": "revenue_per_person",
            "每人營業利益(仟元)": "operating_profit_per_person",
            "長期資金對固定資產比率": "permanent_capital_to_asset_ratio",
            # 資本結構
            "現金流量比率": "cash_flow_ratio",
            "現金流量允當比率": "cash_flow_adequacy_ratio",
            "現金再投資比率": "cash_re_investment_ratio",
            "利息保障倍數": "interest_coverage_ratio"
        }

        assert 0 < quarter < 5

        year_quarters = [(year, cur_quarter) for cur_quarter in reversed(range(1, quarter + 1))]
        last_year_quarters = [(year - 1, cur_quarter) for cur_quarter in reversed(range(1, 5))]
        last_last_year_quarters = [(year - 2, cur_quarter) for cur_quarter in reversed(range(1, 5))]
        next_8_quarters = [*year_quarters, *last_year_quarters, *last_last_year_quarters][:8]

        response = requests.post(self.url["financial"].format(year, quarter, stock_id), data={"is_check": "1"})

        soup = BeautifulSoup(response.text, 'html.parser')

        grade_th = soup.find("th", text="科目名稱")
        assert grade_th is not None

        th_tr = grade_th.find_parent("tr")
        assert th_tr is not None

        assert [th.text for th in th_tr.find_all("th")] == \
               ["科目名稱", *["{}年第{}季".format(cur_year, cur_quarter) for cur_year, cur_quarter in next_8_quarters]]

        trs = [tr for tr in th_tr.find_next_siblings()]
        assert len(trs) == len(financial_key_grade.keys())

        financial = {
            year: {cur_quarter: dict() for cur_year, cur_quarter in next_8_quarters if cur_year == year},
            year - 1: {cur_quarter: dict() for cur_year, cur_quarter in next_8_quarters if cur_year == year - 1},
            year - 2: {cur_quarter: dict() for cur_year, cur_quarter in next_8_quarters if cur_year == year - 2},
        }
        for i, tr in enumerate(trs):
            leading_col, grade, values = get_financial(tr)

            assert leading_col == expect_leading_col.get(i, None)
            assert len(values) == 8

            financial_key = financial_key_grade[grade]
            for j, financial_value in enumerate(values):
                cur_year, cur_quarter = next_8_quarters[j]
                assert financial_key not in financial[cur_year][cur_quarter]
                financial[cur_year][cur_quarter][financial_key] = financial_value
        return financial


def get_month_revenue(tr) -> (int, StockDataMonthRevenue):
    tds = [td for td in tr.find_all("td")]
    assert len(tds) == 9

    if tds[1].text == "":
        return None, None
    else:
        return int(tds[0].text), {
            "revenue":                        round(float(tds[1].text.replace(",", ""))),
            "year_increase_rate":             float(tds[2].text.replace("%", "")),
            "incremental":                    round(float(tds[3].text.replace(",", ""))),
            "incremental_year_increase_rate": float(tds[4].text.replace("%", ""))
        }


def get_financial(tr):
    tds = [td for td in tr.find_all("td")]

    assert len(tds) == 9 or len(tds) == 10
    if len(tds) == 9:
        return None, tds[0].text, [None if tds[i].text == "-" else float(tds[i].text) for i in range(1, 9)]
    else:
        # len(tds) == 10
        return tds[0].text, tds[1].text, [None if tds[i].text == "-" else float(tds[i].text) for i in range(2, 10)]


if __name__ == '__main__':
    a = StockDataSourcePcHome()
    print(a.get_revenue(2330, 2021))
    print(a.get_financial(2330, 2020, 2))
