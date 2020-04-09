from tools import bilibili_repitle
import time

# 新建一个爬虫工具repitle
repitle = bilibili_repitle.bilibili_reptile()

av_start = 99999898
av_end = 99999998

success_sum = 0
total_sum = av_end-av_start+1

s_time = time.perf_counter()
for i in range(av_start, av_end+1):
    repitle.set_bv(i)
    # 写入数据库
    repitle.to_table()
    # 记录完成百分比
    print("Finish " + str(round((i-av_start)*100/total_sum, 2)) + "%")
e_time = time.perf_counter()
# 打印写入数量
print("Finish "+str(repitle.sum_table_3)+" items inserted into b3_qgfx ")
print("Finish "+str(repitle.sum_table_4)+" items inserted into hd_cyfx")
print("Total time cost is : "+str(round(e_time-s_time, 4))+"s")

