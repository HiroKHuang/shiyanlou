# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy.orm import sessionmaker
from shiyanlouUser.models import User, engine
from shiyanlouUser.items import UserItem

print(engine)
class ShiyanlouuserPipeline(object):
    def process_item(self, item, spider):
        item['level'] = int(item['level'][1:])
        item['join_date'] = datetime.strptime(item['join_date'].split()[0],'%Y-%m-%d').date()
        item['learn_courses_num'] = int(item['learn_courses_num'])
        self.session.add(User(**item))

    def open_spider(self, spider):
        Session = sessionmaker(bind=engine)
        self.session=Session()

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()
