#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : xinxi
@Time    : 2018/12/5 18:34
@describe: 获取fps
当渲染时间大于16.67，按照垂直同步机制，该帧就已经渲染超时
那么，如果它正好是16.67的整数倍，比如66.68，则它花费了4个垂直同步脉冲，减去本身需要一个，则超时3个
如果它不是16.67的整数倍，比如67，那么它花费的垂直同步脉冲应向上取整，即5个，减去本身需要一个，即超时4个，可直接算向下取整
最后的计算方法思路：
执行一次命令，总共收集到了m帧（理想情况下m=128），但是这m帧里面有些帧渲染超过了16.67毫秒，算一次jank，一旦jank，
需要用掉额外的垂直同步脉冲。其他的就算没有超过16.67，也按一个脉冲时间来算（理想情况下，一个脉冲就可以渲染完一帧）
所以FPS的算法可以变为：
m / （m + 额外的垂直同步脉冲） * 60
"""

import os,re,time,sys
from wsgiref.validate import validator
sys.path.append('..')
reload(sys)
sys.setdefaultencoding("utf-8")
from ..config import fps_path
from ..tools.loggers import JFMlogging
logger = JFMlogging().getloger()
from ..tools.filetools import write_file


class GetFPS():

    def __init__(self, device_name,activity,pck_name):
        self.device_name = device_name
        self.activity = activity
        self.pck_name = pck_name

    def getfps(self):
        '''
        计算fps
        :return:
        '''
        fps = 0
        try:
            cmd = "adb -s %s shell dumpsys gfxinfo %s" % (self.device_name,self.pck_name)
            result = os.popen(cmd).read().strip()
            frames = [x for x in result.split('\n') if validator(x)]
            frame_count = len(frames)
            jank_count = 0
            vsync_overtime = 0
            render_time = 0
            for frame in frames:
                time_block = re.split(r'\s+', frame.strip())
                if len(time_block) == 3:
                    try:
                        render_time = float(time_block[0]) + float(time_block[1]) + float(time_block[2])
                    except Exception as e:
                        render_time = 0
                if render_time > 16.67:
                    jank_count += 1
                    if render_time % 16.67 == 0:
                        vsync_overtime += int(render_time / 16.67) - 1
                    else:
                        vsync_overtime += int(render_time / 16.67)
            fps = int(frame_count * 60 / (frame_count + vsync_overtime))
        except Exception, e:
            logger.error("获取fps失败:{}".format(e))
        finally:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            info = current_time + ',' + str(fps) + ',' + self.activity + '\n'
            write_file(fps_path, info, is_cover=False)




