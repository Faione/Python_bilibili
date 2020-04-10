from tools import bilibili_crawler
import time

# 新建一个爬虫工具crawler
crawler = bilibili_crawler.bilibili_reptile()

av_start = 99999898
branch = 10
total_sum = 100
wrong_av = []
branch_sum = int(total_sum / branch)

s_time = time.perf_counter()
for i in range(1, branch + 1):
    for av in range(av_start, av_start + branch_sum):
        try:
            crawler.set_bv(av)
            # 写入数据库
            crawler.to_table()
            # 记录完成百分比
            print("Finish branch " + str(i) + " " + str(round((av-av_start+1) * 100 / branch_sum, 2)) + "%")
        except Exception as err:
            # 记录错误branch
            print('Err %s' % err)
            print("Failed at branch " + str(i) + " av is :"+str(av_start))
            wrong_av.append(av)
    print("\nFinish total " + str(round(i * 100 / branch, 2)) + "%\n")
    av_start = av_start + branch_sum
e_time = time.perf_counter()

# 打印写入数量
print("Finish " + str(crawler.sum_table_3) + " items inserted into b3_qgfx ")
print("Finish " + str(crawler.sum_table_4) + " items inserted into hd_cyfx")
print("Total time cost is : " + str(round(e_time - s_time, 4)) + "s")
