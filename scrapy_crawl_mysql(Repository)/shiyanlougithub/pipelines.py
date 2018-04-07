# -*- coding: utf-8 -*-

from shiyanlougithub.items import ShiyanlougithubItem
from shiyanlougithub.models import engine, Repository
from sqlalchemy.orm import sessionmaker
from datetime import datetime

class ShiyanlougithubPipeline(object):
    def process_item(self, item, spider):
        item['update_time']=datetime.strptime(item['update_time'].split('T')[0], '%Y-%m-%d').date()
        self.session.add(Repository(**item))

    def open_spider(self, spider):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()


