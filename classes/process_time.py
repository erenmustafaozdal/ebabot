import time
import classes.log as log

# 4000 kişiden fazla oy kullanan öğretmenin ortalaması:
# 1 ders için 113 saniye zaman harcanıyor
normal_lesson_time = 113

class ProcessTime(object):
    """docstring for ProcessTime"""
    def __init__(self):
        super(ProcessTime, self).__init__()

    def startTime(self):
        self.start_time = time.time()
        print("")
        log.write("-----------------------------------------------")
        log.write("Başlangıç Zamanı: {}".format(time.strftime("%d.%m.%Y, %H:%M:%S", time.localtime())))
        log.write("-----------------------------------------------")
        print("")

    def finishTime(self, lessons_count, isDelete = False):
        finish_time = time.time()
        time_text = time.strftime("%d.%m.%Y, %H:%M:%S",time.localtime())
        diff_seconds = finish_time-self.start_time
        process = time.strftime('%H:%M:%S', time.gmtime(diff_seconds))
        print("")
        log.write("-----------------------------------------------")
        log.write("Bitiş Zamanı: {}".format(time_text))
        log.write("-----------------------------------------------")
        log.write("Toplam Süre: {}".format(process))
        log.write("-----------------------------------------------")

        if isDelete == False:
            time_saved = time.strftime('%H:%M:%S', time.gmtime((lessons_count*normal_lesson_time) - diff_seconds))
            log.write("EBABOT ile {} süre kazandınız :)".format(time_saved))
            log.write("-----------------------------------------------")
        print("")
