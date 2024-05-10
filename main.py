from lottery_history import TaiwanLotteryHistoryCrawler
import asyncio


async def gather_lottery_data():
    crawler = TaiwanLotteryHistoryCrawler()
    # super_lotto = crawler.get_super_lottery_history(begin_year=112, end_month=10)
    # big_lotto = crawler.get_Lotto_lottery_history(begin_year=112, end_month=10)
    # _539_lotto = crawler.get_539_lottery_history(begin_year=112, end_month=10)
    # winwin_lotto = crawler.get_winwin_lottery_history(begin_year=112, end_month=10)
    # _3star_lotto = crawler.get_3star_lottery_history(begin_year=112, end_month=10)
    _4star_lotto = crawler.get_4star_lottery_history(begin_year=112, end_month=10)
    await asyncio.gather( _4star_lotto)


if __name__ == '__main__':
    # await crawler.get_super_lottery_history(begin_year=112, end_month=12)
    # crawler = TaiwanLotteryHistoryCrawler()
    asyncio.run(gather_lottery_data())
