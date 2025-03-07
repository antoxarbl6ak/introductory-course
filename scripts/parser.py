import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

driver = webdriver.Edge()
driver.get(r"https://patentscope.wipo.int/search/ru/advancedSearch.jsf")
time.sleep(9)

driver.find_element(By.CLASS_NAME, "ps-office--input").click()
time.sleep(2)
for opt in driver.find_elements(By.CLASS_NAME, "ps-office--options--item"):
    if opt.text == "Франция":
        opt.find_element(By.TAG_NAME, "input").click()
        break

select_lang = Select(driver.find_element(By.ID, "advancedSearchForm:queryLanguage:input"))
select_lang.select_by_value("fr")

search = driver.find_element(By.ID, "advancedSearchForm:searchButton")
search.click()

time.sleep(10)

#select_num_elements = Select(driver.find_element(By.ID, "resultListCommandsForm:perPage:input"))
#select_num_elements.select_by_value("200")
#time.sleep(10)

dataset = []
for i in range(3):
    if i:
        time.sleep(10)
        next_page = driver.find_element(By.XPATH, r'//*[@id="resultListCommandsForm:j_idt2031"]')
        next_page.click()
        time.sleep(5)
    c = 0
    table = driver.find_element(By.ID, "resultListForm:resultTable_data")
    for cell in table.find_elements(By.TAG_NAME, "tr"):
        data_per_cell = {"patent_number": 0,
                        "name": "",
                        "date": "",
                        "application_number": 0,
                        "applicant": "",
                        "inventor": "",
                        "text": ""}
        patent_number = cell.find_element(By.XPATH, fr'//*[@id="resultListForm:resultTable:{c}:patentResult"]/div[1]/div[1]/a/span')
        data_per_cell["patent_number"] = int(patent_number.text)

        name = cell.find_element(By.XPATH, fr'//*[@id="resultListForm:resultTable:{c}:patentResult"]/div[1]/div[1]/span[2]/span')
        data_per_cell["name"] = name.text

        date = cell.find_element(By.XPATH, fr'//*[@id="resultListForm:resultTable:{c}:resultListTableColumnPubDate"]')
        data_per_cell["date"] = date.text

        application_number = cell.find_element(By.XPATH, fr'/html/body/div[2]/div[4]/div/div[1]/div[2]/div/form[2]/div/div[1]/div/div/table/tbody/tr[{c + 1}]/td/div/div[2]/div/div[1]/span[2]/span[2]')
        data_per_cell["application_number"] = int(application_number.text)

        applicant = cell.find_element(By.XPATH, fr'/html/body/div[2]/div[4]/div/div[1]/div[2]/div/form[2]/div/div[1]/div/div/table/tbody/tr[{c + 1}]/td/div/div[2]/div/div[1]/span[3]/span[2]')
        data_per_cell["applicant"] = applicant.text

        inventor = cell.find_element(By.XPATH, fr'/html/body/div[2]/div[4]/div/div[1]/div[2]/div/form[2]/div/div[1]/div/div/table/tbody/tr[{c + 1}]/td/div/div[2]/div/div[1]/span[4]/span[2]')
        data_per_cell["inventor"] = inventor.text

        text = cell.find_element(By.XPATH, fr'/html/body/div[2]/div[4]/div/div[1]/div[2]/div/form[2]/div/div[1]/div/div/table/tbody/tr[{c + 1}]/td/div/div[2]/div/div[2]/span')
        data_per_cell["text"] = text.text

        dataset.append(data_per_cell)
        c += 1

print(dataset[0])
print(dataset[-1])
print(len(dataset))

time.sleep(10)
driver.close()
