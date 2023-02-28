import datetime
import time
from pprint import pprint

import pytz
from dotenv import dotenv_values
from notion_client import Client

config = dotenv_values('private/.env')
client = Client(auth=config.get('NOTION_TOKEN'))
seoul_tz = pytz.timezone('Asia/Seoul')


class Monitor:
    @staticmethod
    def check():
        today_start = datetime.datetime.now(seoul_tz).replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start.replace(hour=23, minute=59, second=59, microsecond=999999)

        results = client.databases.query(
            **{
                'database_id': '7847ac46a31a4317b66ae4e700f55403',
                'filter': {
                    'and': [
                        {
                            'property': '날짜',
                            'date': {
                                'on_or_after': today_start.isoformat()
                            }
                        },
                        {
                            'property': '날짜',
                            'date': {
                                'on_or_before': today_end.isoformat()
                            }
                        }
                    ]
                }
            }
        ).get('results')

        if not results:
            return False  # 할일 미정의 == 미완수

        for task in results:
            if not task.get('properties').get('완료여부').get('formula').get('boolean'):
                return False

        return True

    @staticmethod
    def sleep_until(hour: int):
        now = datetime.datetime.now()

        if now.hour < 8:
            target_time = datetime.datetime.combine(now.date(), datetime.time(hour))
        else:
            tomorrow = now + datetime.timedelta(days=1)
            target_time = datetime.datetime.combine(tomorrow.date(), datetime.time(hour))
        delta_t = target_time - now
        time.sleep(delta_t.seconds)

    @staticmethod
    def sleep(seconds: float):
        time.sleep(seconds)


if __name__ == '__main__':
    ...
    test = Monitor.check()
    print(test)
