import json
import sys
import codecs
from datetime import datetime

class CrawlerperiodicosPipeline(object):

    flgFirstItem = True

    def open_spider(self, spider):

        if spider.strFile == "":
            return
        
        self.file = codecs.open(spider.strFile, 'w', encoding='utf-8') 
        self.file.write("[\n")
        

    def close_spider(self, spider):

        if spider.strFile == "":
            return
            
        self.file.write("\n]")
        self.file.close()

    def process_item(self, item, spider):
        
        if self.flgFirstItem == False:
            self.file.write(",\n")

        line = json.dumps(dict(item), ensure_ascii=False, indent=4)
        self.file.write(line)

        self.flgFirstItem = False

        return item