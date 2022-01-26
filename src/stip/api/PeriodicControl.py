import re
from datetime import datetime

class PeriodicControl:
    def __init__(self):
        pass

    def judgeToPublishTarget(self, receive_frequency, subscribe_start_time):
        now = datetime.now()
        now_minute = int(now.minute)
        now_hour  = int(now.hour)

        receive_frequency = receive_frequency.split()
        minute_part = int(receive_frequency[0])
        hour_part = int(receive_frequency[1])
        # 時間の対象における一致を確認し，一致しなかった場合は処理を終了
        if (not self.chechMatchHour(now_hour, hour_part)): return False

        # 分単位の周期チェックを行い，一致したらTrue, 一致しない場合はFalseを返す
        return self.checkMatchMinute(now_hour, now_minute, hour_part, minute_part, subscribe_start_time)
    

    # 一旦，,と-の複雑な組み合わせについては検討とする
    def checkMatchHour(self, now_hour, hour_part):
        if ("*" in hour_part): 
            return True

        if ("," in hour_part):
            hour_part = hour_part.split(",")
            # ,の場合は複数個含まれている可能性があるため，for文で回す
            for each_hour in hour_part:
                if (int(each_hour) == now_hour):
                    return True

        if ("-" in hour_part):
            hour_part = hour_part.split("-")
            if (int(hour_part[0]) <= now_hour <= int(hour_part[1])):
                return True

        return False

    # サブスクライブ登録した時間を用いて表現できる
    # (now_hour*60 + now_minute) 
    #   - (subscribe_start_time.hour*60 + subscribe_start_time.minute) % min_part == 0
    # 時間の期間に収まっているか，複数してしたどれと一致しているかは上で判定しているため，不要
    def checkMatchMinute(self, now_hour, now_minute, min_part, subscribe_start_time):
        # Subsciber_Topicを登録した時間
        dt_subscribe_start_time = datetime.strptime(subscribe_start_time, '%Y-%m-%d %H:%M:%S')
        if ( (now_hour*60 + now_minute) 
            - (dt_subscribe_start_time.hour*60 + dt_subscribe_start_time.minute) % min_part == 0):
            return True
        return False