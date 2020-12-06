from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import settings
import classes.log as log
import time

web_wait = settings.web_implicitly_wait

class Zoom(object):
    """docstring for Zoom"""
    def __init__(self, web):
        super(Zoom, self).__init__()
        self.__web = web
        self.__driver = self.__web.get()

    def getSchedule(self):
        self.__driver.get("https://us04web.zoom.us/meeting/schedule")

    def getUpcomingMeetings(self):
        self.__driver.get("https://us04web.zoom.us/meeting#/upcoming")

    def getSettingMeeting(self):
        self.__driver.get("https://us04web.zoom.us/profile/setting?tab=meeting")

    def getSettingRecording(self):
        self.__driver.get("https://us04web.zoom.us/profile/setting?tab=recording")

    def waitForSignIn(self, user):
        if "signin" in self.__driver.current_url:
            log.write("Zoom'a giriş yapılmamış.", "error")
            log.write("Lütfen <red>Zoom</>'a <green>300 saniye</> içinde giriş yapın.", "header")
            self.login(user)
            self.__web.wait(EC.element_to_be_clickable((By.ID, 'meetingSaveButton')))
            log.write("<green>Zoom'a giriş yapıldı.</>", "header")

    def login(self, user):
        email = self.__web.element("//*[@id='email']")
        email.send_keys(user['zoom_email'])
        password = self.__web.element("//*[@id='password']")
        password.send_keys(user['zoom_password'])

    def lessonMeta(self, lesson):
        topic = self.__web.element("//*[@id='topic']")
        topic.clear()
        topic.send_keys(lesson['Canlı Ders Başlığı'])
        self.__web.element("//*[@id='agenda']").send_keys(lesson['Açıklama'])

    def lessonDate(self, lesson, xl):
        day = xl.getDayOfDateString(lesson['Canlı Ders Tarihi'])
        self.__web.element("//*[@id=\"mt_time\"]/div[1]/div/button").click()
        dayBtnXPATH = "//*[@id=\"ui-datepicker-div\"]/table/tbody/tr/td[@data-event='click']/a[text() = '{}']".format(day)
        dayBtn = self.__web.element(dayBtnXPATH)
        # eğer yeni aya girmeden, sonraki aydan bir gün seçilmek isteniyorsa
        if dayBtn == False:
            self.__web.element("//*[@id=\"ui-datepicker-div\"]/*/a[@data-handler=\"next\"]").click()
            dayBtn = self.__web.element(dayBtnXPATH)

        dayBtn.click()


    def lessonHour(self, lesson, xl):
        hour = xl.getHourString(lesson['Ders Başlangıç'])
        self.__web.element("//*[@id=\"mt_time\"]/div[1]/div/div/div/div").click()
        self.__web.element("//*/input[@aria-owns='start_time-popup-list']").send_keys(hour)
        self.__web.element("//*[@id=\"start_time-popup-list\"]/dd[@option-id='{}']".format(hour)).click()

    def lessonTime(self, lesson):
        # self.__web.element("//*[@id=\"mt_time\"]/div[2]/div[2]/div[1]/div[1]").click()
        self.__web.wait(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"mt_time\"]/div[2]/div[2]/div[1]/div[1]")), 5).click()
        element = self.__web.wait(EC.element_to_be_clickable((By.ID, 'select-item-duration_hr-0')), 5)
        element.click()

        # self.__web.element("//*[@id=\"mt_time\"]/div[2]/div[2]/div[1]/div[2]").click()
        self.__web.wait(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"mt_time\"]/div[2]/div[2]/div[1]/div[2]")), 5).click()
        element = self.__web.wait(EC.element_to_be_clickable((By.ID, 'select-item-duration_min-2')), 5)
        element.click()

    def meetingID(self, lesson):
        if lesson['Meeting ID'] == 'pmi':
            self.__web.element("//*/input[@id=\"optionScheduleWithPMI\"]").click()
        else:
            self.__web.element("//*/input[@id=\"optionOneTimeId\"]").click()

    def meetingPasscode(self, lesson):
        if lesson['Passcode'] != '':
            self.__web.element("//*/input[@id=\"meeting_pass\"]").clear()
            self.__web.element("//*/input[@id=\"meeting_pass\"]").send_keys(lesson['Passcode'])

    def waitingRoom(self, lesson):
        checkbox = self.__web.element("//*/input[@id=\"option_waiting_room\"]")
        if lesson['Waiting Room'] == 'on':
            if not checkbox.is_selected():
                checkbox.click()
        else:
            if checkbox.is_selected():
                checkbox.click()

    def videoHost(self, lesson):
        if lesson['Video Host'] == 'on':
            self.__web.element("//*/input[@id=\"option_video_host_on\"]").click()
        else:
            self.__web.element("//*/input[@id=\"option_video_host_off\"]").click()

    def videoParticipant(self, lesson):
        if lesson['Video Participant'] == 'on':
            self.__web.element("//*/input[@id=\"option_video_participant_on\"]").click()
        else:
            self.__web.element("//*/input[@id=\"option_video_participant_off\"]").click()

    def setRequestUnmuteSettingOn(self):
        self.getSettingMeeting()
        self.__web.element("//div[@id=\"feature-requestPermission2Unmute\"]//label[@class=\"zm-switch\"]").click()
        self.__web.wait(EC.visibility_of_element_located((By.XPATH, '//*[contains(text(), "Your settings have been updated.")]')))
        log.write("Zoom'da Request Unmute ayarı açıldı.", "header")

    def requestUnmute(self, lesson):
        checkbox = self.__web.element("//*/input[@id=\"option_request_unmute_all\"]")
        if lesson['Request Unmute'] == 'on':
            if checkbox.is_displayed() == False:
                return "repeat"
            if not checkbox.is_selected():
                checkbox.click()
        else:
            if checkbox.is_displayed() and checkbox.is_selected():
                checkbox.click()

    def setAutoRecordSettingOn(self):
        self.getSettingRecording()
        self.__web.element("//div[@id=\"feature-localrecording\"]//label[@class=\"zm-switch\"]").click()
        # time.sleep(0.2)
        # self.__web.element("//*[contains(text(), 'Turn On')]").click()
        # time.sleep(0.2)

        self.__web.wait(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Turn On')]")), 1).click()
        self.__web.wait(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Turn On')]")), 2, True)
        self.__web.wait(EC.visibility_of_element_located((By.XPATH, '//*[contains(text(), "Your settings have been updated.")]')))
        time.sleep(3)
        self.__web.element("//div[@id=\"feature-autorecording\"]//label[@class=\"zm-switch\"]").click()
        self.__web.wait(EC.visibility_of_element_located((By.XPATH, '//*[contains(text(), "Your settings have been updated.")]')))
        log.write("Zoom'da Auto Record ayarı açıldı.", "header")

    def autoRecord(self, lesson):
        checkbox = self.__web.element("//*/input[@id=\"option_autorec\"]")
        if lesson['Auto Record'] == 'on':
            if checkbox == False:
                return "repeat"
            if not checkbox.is_selected():
                checkbox.click()
        else:
            if checkbox and checkbox.is_selected():
                checkbox.click()

    def lessonSave(self, lesson, xl):
        self.__web.switchTab(0)
        self.getSchedule()

        isRepeat = False
        reqUnResult = self.requestUnmute(lesson)
        auRecResult = self.autoRecord(lesson)
        if reqUnResult == "repeat":
            isRepeat = True
            self.setRequestUnmuteSettingOn()
        if auRecResult == "repeat":
            isRepeat = True
            self.setAutoRecordSettingOn()
        if isRepeat == True:
            self.lessonSave(lesson, xl)
            return

        self.lessonMeta(lesson)
        self.lessonDate(lesson,xl)
        self.lessonHour(lesson,xl)
        # time.sleep(0.5)
        self.lessonTime(lesson)
        self.meetingID(lesson)
        self.meetingPasscode(lesson)
        self.waitingRoom(lesson)
        self.videoHost(lesson)
        self.videoParticipant(lesson)

        self.__web.element("//*[@id=\"meetingSaveButton\"]").click()

        log.write("{}. ders Zoom'da kaydedildi: {} ({}, {} - {})".format(lesson['id'], lesson['Canlı Ders Başlığı'], xl.getDateString(lesson['Canlı Ders Tarihi']), xl.getHourString(lesson['Ders Başlangıç']), xl.getHourString(lesson['Ders Bitiş'])))

        lesson['link'] = self.__web.element("//*[@id=\"info_form\"]/div[5]/div/div/span[1]").text
        self.__web.element("//*[@id=\"showPassword\"]").click()
        lesson['passcode'] = self.__web.element("//*[@id=\"displayPassword\"]").text

    def lessonDelete(self):
        lesson_link = self.__web.wait(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/div/div[4]/div/div[1]/div[2]/div/div/div/div[1]/div/div[2]/div[1]/div[2]/a')), 1)

        if lesson_link == False:
            return False

        hour = self.__web.wait(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div/div[4]/div/div[1]/div[2]/div/div/div/div[1]/div/div[2]/div[1]/div[1]/div/span'))).text
        lesson = lesson_link.text

        time.sleep(float(web_wait)/6)
        lesson_link.click()
        date = self.__web.element("//*[@id=\"info_form\"]/div[2]/div/div/div[1]").text.split(",")[0]
        self.__web.wait(EC.element_to_be_clickable((By.ID, 'btn_Delete_meeting')), 1).click()
        time.sleep(float(web_wait)/6)
        self.__web.wait(EC.element_to_be_clickable((By.ID, 'submitDeleteEndBtn')), 1).click()

        log.write("Ders silindi: {} ({}, {})".format(lesson, date, hour))


    def lessonsDelete(self):
        self.__web.switchTab(0)
        self.getUpcomingMeetings()

        log.write("Zoom'da dersleri silme işlemi başlıyor.", "header")

        while True:
            if self.lessonDelete() == False:
                break

        log.write("Zoom'da dersleri silme işlemi başarılı bir şekilde tamamlandı.", "header")


