from logging import info

from utils import *

setup('https://URL.com')
info('done opening url')

switch_frame('frmRIGHT')
info('swtich to frmRIGHT')

update_select_value("#chotatsuType", "物品等")

find("#link2").click()
info('redirect to search page')

update_select_value("A300", "100")

update_select_value("A103", "電算業務")
run_script("doSearch1()")
# 省略〜