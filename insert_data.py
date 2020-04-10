from tools import bilibili_crawler
import time

# 新建一个爬虫工具crawler
crawler = bilibili_crawler.bilibili_reptile()

# 记录出错av号，set_bv后用crawler.get_origin_url() 获得出错av号的页面
wrong_av = []

# 起始av号码
av_start = 99999898
# 总共爬取数量
total_sum = 100
# 分成多少次进行爬取, 一次性运行设置为1
branch = 6
# 每次爬取多少个av号
branch_sum = int(total_sum / branch)

# 中断操作
# 务必在一个branch完成后中断
# branch_cut 初值为0
# branch_cut = 中断前的已经完成的branch
# 重设branc_cut 值继续爬取
branch_cut = 0

continue_branch = branch_cut + 1
continue_av_start = branch_cut * branch_sum + av_start

s_time = time.perf_counter()
for i in range(continue_branch, branch + 1):
    print("Start...")
    for av in range(continue_av_start, continue_av_start + branch_sum):
        try:
            # 获得bv号
            crawler.set_bv(av)
            # 写入数据库
            crawler.to_table()
            # 记录完成百分比
            print("Finish branch " + str(i)+": "+str(round((av - continue_av_start + 1) * 100 / branch_sum, 2)) + "%")

        except Exception as err:

            print('Err %s' % err)
            print("Failed at branch " + str(i))
            # 记录错误av号
            wrong_av.append(av)

    print("\nFinish total " + str(round(i * 100 / branch, 2)) + "%\n")

# 停止处理
    continue_check = input("继续爬取请按回车, 退出则输入#: ")
    if continue_check == "#":
        if len(wrong_av) != 0:
            print("没有发生错误")
        else:
            for err_av in wrong_av:
                print("出现错误的av号: "+err_av)

        print("完成branch " + str(i) + " 后停止", "\n再次运行时请重设branch_cut为: " + str(i))
        break
    continue_av_start = continue_av_start + branch_sum

e_time = time.perf_counter()

# 打印写入数量
print("\nFinish " + str(crawler.sum_table_3) + " items inserted into b3_qgfx ")
print("Finish " + str(crawler.sum_table_4) + " items inserted into hd_cyfx")
print("Total time cost is : " + str(round(e_time - s_time, 4)) + "s")
