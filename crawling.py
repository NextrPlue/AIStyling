from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import urllib.request
import os

# 검색쿼리
searchKey = input('검색할 키워드 입력 :')
searchNum = input('저장할 사진의 개수 입력 :')

# 폴더 생성
def createFolder(dir):
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
    except OSError:
        print('Error')

createFolder(f'train_dataset/{searchKey}')

# 크롬 드라이버 생성
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)
driver.get('https://www.google.com/imghp?hl=ko&tab=ri&authuser=0&ogbl')

# 쿼리 검색 및 검색 버튼 클릭
elem = driver.find_element('name', 'q')
elem.send_keys(searchKey)
elem.send_keys(Keys.RETURN)

time.sleep(1)

# 이미지 스크롤링
count = 1
while True:
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);') # 브라우저 끝까지 스크롤
    count += 1
    print(count)
    time.sleep(2) # 쉬어주기
    try:
        button = driver.find_element(By.XPATH, '//*[@id="islmp"]/div/div/div/div/div[1]/div[2]/div[2]/input')
        button.click() # 스크롤을 내리다보면 '결과 더보기'가 있는 경우 버튼 클릭
        time.sleep(2)
    except:
        pass
    if count == 10: # class 이름으로 가져오기
        break

# 이미지 수집 및 저장
images = driver.find_elements(By.CSS_SELECTOR, ".YQ4gaf") # 각 이미지들의 class
associations = driver.find_elements(By.CSS_SELECTOR, ".YQ4gaf.zr758c.wA1Bge")
images = [x for x in images if x not in associations]

if images == []:
    print("error")
    driver.close()
    quit()

count = 1
for i in range(len(images)):
    if count > int(searchNum):
        break
    try:
        images[i].click()
        time.sleep(1)
        if len(driver.window_handles) == 1:
            imgUrl = driver.find_element(By.XPATH,
                '//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div/div[3]/div[1]/a/img[1]').get_attribute("src")
            imgUrl = imgUrl.replace('https', 'http') # https로 요청할 경우 보안 문제로 SSL에러가 남
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-Agent', 'Mozilla/5.0')] # https://docs.python.org/3/library/urllib.request.html 참고
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(imgUrl, f'train_dataset/{searchKey}/{searchKey}_{str(int(i/2 + 1))}.jpg') # url을 
            print(f'--{count}번째 이미지 저장 완료--')
            count += 1
        else:
            driver.switch_to.window(driver.window_handles[-1])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
    except Exception as e:
        print('Error : ', e)
        pass

driver.close()
quit()
