from typing import TypedDict, Optional, Tuple, NewType


class StockDataMonthRevenue(TypedDict):
    revenue: int
    year_increase_rate: float
    incremental: int
    incremental_year_increase_rate: float


StockDataYearRevenue = Tuple[Optional[StockDataMonthRevenue], Optional[StockDataMonthRevenue],
                             Optional[StockDataMonthRevenue], Optional[StockDataMonthRevenue],
                             Optional[StockDataMonthRevenue], Optional[StockDataMonthRevenue],
                             Optional[StockDataMonthRevenue], Optional[StockDataMonthRevenue],
                             Optional[StockDataMonthRevenue], Optional[StockDataMonthRevenue],
                             Optional[StockDataMonthRevenue], Optional[StockDataMonthRevenue]]

if __name__ == '__main__':
    b = {
        "revenue": "asd",
        "year_increase_rate": 1.1,
        "incremental": 2,
        "incremental_year_increase_rate": 2.2
    }

    def test_func(a: StockDataYearRevenue):
        print(a)

    test_func(StockDataYearRevenue((StockDataMonthRevenue(b),
               None, None, None,
               None, None, None,
               None, None, None, None, None)))
