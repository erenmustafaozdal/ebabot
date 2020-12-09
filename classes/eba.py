from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import settings
import classes.log as log
import random
import time

user_sign = settings.eba_user_sign
web_wait = settings.web_implicitly_wait

class EBA(object):
    """docstring for EBA"""
    def __init__(self, web):
        super(EBA, self).__init__()
        self.__web = web
        self.__driver = self.__web.get()

    def waitForSignIn(self, user):
        log.write("Lütfen <red>EBA</>'ya <green>300 saniye</> içinde giriş yapın.", "header")
        self.__web.wait(EC.element_to_be_clickable((By.ID, 'vc-treeleftmenu')))

    def login(self, user):
        self.__driver.execute_script("window.open('https://giris.eba.gov.tr/EBA_GIRIS/teacher.jsp');")
        self.__web.switchTab(-1)
        edevlet_btn = self.__web.wait(EC.element_to_be_clickable((By.XPATH, '//*/button[@title="edevlet girişi"]')), 1)

        if edevlet_btn == False:
            return
        edevlet_btn.click()

        self.__web.element("//*/input[@id=\"tridField\"]").send_keys(user['edevlet_tc'])
        self.__web.element("//*/input[@id=\"egpField\"]").send_keys(user['edevlet_password'])

        if user['edevlet_tc'] == "" or user['edevlet_password'] == "":
            self.waitForSignIn(user)
        elif user_sign:
            self.waitForSignIn(user)
        else:
            self.__web.element("//*/input[@name=\"submitButton\"]").click()
        self.__web.wait(EC.element_to_be_clickable((By.ID, 'vc-treeleftmenu')))
        log.write("<green>EBA'ya giriş yapıldı.</>", "header")

    def getLessonSave(self):
        self.__driver.get("https://ders.eba.gov.tr/ders/proxy/VCollabPlayer_v0.0.746/index.html#/main/editExternalLiveSession")

    def getExternalLessons(self):
        self.__driver.get("https://ders.eba.gov.tr/ders/proxy/VCollabPlayer_v0.0.746/index.html#/main/livesessionview?tab=externalLiveLessons&pageNumber=1&pageSize=25")

    def lessonMeta(self, lesson):
        #self.__web.element("//*[contains(text(), 'Ders Başlığı')]/following-sibling::input[1]").send_keys(lesson['Canlı Ders Başlığı'])
        self.__web.wait(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Ders Başlığı')]/following-sibling::input[1]")), 5).send_keys(lesson['Canlı Ders Başlığı'])
        self.__web.element("//*[contains(text(), 'Sınıf')]/following-sibling::select[1]//option[text()='{}']".format(lesson['Sınıf'])).click()

    def lessonDate(self, lesson, xl):
        day = xl.getDayOfDateString(lesson['Canlı Ders Tarihi'], True)
        self.__web.element("//*[@id=\"ebaEtudEditView\"]/div[2]/div/div/div[1]/div[1]/div[2]/div[3]/p/span").click()
        self.__web.element("//*/table[@class='uib-daypicker']//button[not(@disabled)]/span[contains(text(),'{}')]".format(day)).click()

    def lessonHour(self, lesson, xl):
        hour = xl.getHourString(lesson['Ders Başlangıç'])
        f_hour = xl.getHourString(lesson['Ders Bitiş'])
        element = self.__web.wait(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Saat Aralığı')]/following-sibling::div[1]//option[text()='{} - {}']".format(hour, f_hour))), 5)
        # element = self.__web.wait(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Saat Aralığı')]/following-sibling::div[1]//option[text()='{} - {}']".format(hour, f_hour))), 5)
        element.click()

    def lessonDetail(self, lesson):
        self.__web.element("//*[contains(text(), 'Açıklama')]/following-sibling::input[1]").send_keys(lesson['Açıklama'])
        self.__web.element("//*[contains(text(), 'Link')]/following-sibling::input[1]").send_keys(lesson['link'])
        self.__web.element("//*[contains(text(), 'Şifre')]/following-sibling::input[1]").send_keys(lesson['passcode'])

    def lessonName(self, lesson):
        self.__web.element("//*[contains(text(), 'Ders *')]/following-sibling::div[1]/div[1]").click()
        self.__web.wait(EC.element_to_be_clickable((By.XPATH, '//*[text()="Ders *"]/following-sibling::div//*[text()="{}"]'.format(lesson['Ders']))), 5).click()
        #self.__web.element("//*[contains(text(), '{}')]".format(lesson['Ders'])).click()


    def lessonUnit(self, lesson):
        if lesson['Ünite'] == "":
            return

        self.__web.wait(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Ünite')]/following-sibling::select[1]//option[text()='{}']".format(lesson['Ünite']))), 5).click()
        # self.__web.element("//*[contains(text(), 'Ünite')]/following-sibling::select[1]//option[text()='{}']".format(lesson['Ünite'])).click()


    def lessonSubject(self, lesson):
        if lesson['Konu'] == "":
            return

        self.__web.wait(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Konu')]/following-sibling::select[1]//option[text()='{}']".format(lesson['Konu']))), 5).click()
        # self.__web.element("//*[contains(text(), 'Konu')]/following-sibling::select[1]//option[text()='{}']".format(lesson['Konu'])).click()

    def lessonClass(self, lesson):
        #self.__web.element("//*[contains(text(), 'Şube/Grup')]/parent::div/following-sibling::div[1]").click()
        time.sleep(float(web_wait)/6)
        self.__web.wait(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Şube/Grup')]/parent::div/following-sibling::div[1]")), 5).click()
        for group in lesson['Şube/Grup'].split(","):
            self.__web.wait(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), '{}')]".format(group))), 5).click()
            #self.__web.element("//*[contains(text(), '" + group + "')]").click()


    def lessonSave(self, lesson, xl):
        self.__web.switchTab(1)
        self.getLessonSave()

        self.lessonMeta(lesson)
        self.lessonDate(lesson, xl)
        time.sleep(float(web_wait)/6)
        self.lessonHour(lesson, xl)
        self.lessonDetail(lesson)
        self.lessonName(lesson)
        time.sleep(float(web_wait)/6)
        self.lessonUnit(lesson)
        time.sleep(float(web_wait)/6)
        self.lessonSubject(lesson)
        self.lessonClass(lesson)


        self.__web.element("//*[contains(text(), 'ÖĞRENCİLERİ LİSTELE')]").click()
        time.sleep(float(web_wait)/6)
        # self.__web.element("//*[contains(text(), 'CANLI DERSİ GÖNDER')]").click()
        self.__web.wait(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'CANLI DERSİ GÖNDER')]")), 5).click()
        time.sleep(float(web_wait)/6)
        # self.__web.element("//*[contains(text(), 'TAMAM')]").click()
        self.__web.wait(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'TAMAM')]")), 5).click()

        log.write("{}. ders EBA'da kaydedildi: {} ({}, {} - {})".format(lesson['id'], lesson['Canlı Ders Başlığı'], xl.getDateString(lesson['Canlı Ders Tarihi']), xl.getHourString(lesson['Ders Başlangıç']), xl.getHourString(lesson['Ders Bitiş'])))

    def lessonDelete(self):
        lesson_btn_group = self.__web.wait(EC.element_to_be_clickable((By.XPATH, '//*[@id="liveLessonList"]/div[2]/div/div[3]/div/div[3]/div[1]/div[2]/div[1]/div/div[7]')), 1)

        if lesson_btn_group == False:
            return False

        date_element = self.__web.wait(EC.visibility_of_element_located((By.XPATH, '//*[@id="liveLessonList"]/div[2]/div/div[3]/div/div[3]/div[1]/div[2]/div[1]/div/div[5]/div/div[1]/div')), 1)
        date = date_element.text.replace("\n", ", ")
        lesson = self.__web.wait(EC.visibility_of_element_located((By.XPATH, '//*[@id="liveLessonList"]/div[2]/div/div[3]/div/div[3]/div[1]/div[2]/div[1]/div/div[1]/div/div[1]/div')), 1).text

        lesson_btn_group.click()
        delete_btn = self.__web.wait(EC.element_to_be_clickable((By.XPATH, '//*/a[contains(text(), "Sil")]')), 1)

        if delete_btn == False:
            log.write("Ders çok yakın, silinemedi: {} ({})".format(lesson, date), "error")
            return

        delete_btn.click()
        self.__web.wait(EC.element_to_be_clickable((By.XPATH, '//*/a[contains(text(), "EVET")]')), 1).click()

        self.__web.wait(EC.visibility_of_element_located((By.XPATH, '//*/div[contains(text(), "Canlı ders başarı ile silindi")]')))
        dates = date_element.text.split("\n")
        self.__web.wait(EC.presence_of_element_located((By.XPATH, "//*/div[contains(text(),'{}') and contains(.,'{}')]".format(dates[0], dates[1]))), 300, True)
        self.__web.wait(EC.presence_of_element_located((By.XPATH, '//*/div[contains(text(), "Canlı ders başarı ile silindi")]')), 300, True)

        log.write("Ders silindi: {} ({})".format(lesson, date))

    def lessonsDelete(self):
        self.__web.switchTab(1)
        self.getExternalLessons()

        log.write("EBA'da dersleri silme işlemi başlıyor.", "header")

        while True:
            if self.lessonDelete() == False:
                break

        log.write("EBA'da dersleri silme işlemi başarılı bir şekilde tamamlandı.", "header")
