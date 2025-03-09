from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.expected_conditions import text_to_be_present_in_element
import pandas as pd

keys = ['publication number',
        'name',
        'date of publication',
        'ipc',
        'application number',
        'applicant',
        'inventor',
        'patent']


driver = webdriver.Chrome()
driver.get(r"https://patentscope.wipo.int/search/ru/advancedSearch.jsf")

WebDriverWait(driver, 20).until(presence_of_element_located((By.CLASS_NAME, "ps-office--input")))
driver.find_element(By.CLASS_NAME, "ps-office--input").click()

for opt in driver.find_elements(By.CLASS_NAME, "ps-office--options--item"):
    if opt.text == "Франция":
        opt.find_element(By.TAG_NAME, "input").click()
        break

select_lang = Select(driver.find_element(By.ID, "advancedSearchForm:queryLanguage:input"))
select_lang.select_by_value("fr")

search = driver.find_element(By.ID, "advancedSearchForm:searchButton")
search.click()

c = 1
WebDriverWait(driver, 20).until(presence_of_element_located((By.ID, "resultListCommandsForm:perPage:input")))
select_num_elements = Select(driver.find_element(By.ID, "resultListCommandsForm:perPage:input"))
select_num_elements.select_by_value("200")
results = []
for i in range(25):
    WebDriverWait(driver, 20).until(
        presence_of_element_located((By.CSS_SELECTOR, '[id="resultListForm:resultTable:199:patentResult"]'))
    )
    table = driver.find_element(By.ID, "resultListForm:resultTable_data")
    for cell in table.find_elements(By.TAG_NAME, "tr"):
        pubnum = cell.find_element(By.TAG_NAME, 'a').text
        name = cell.find_element(By.CSS_SELECTOR, '[class="ps-patent-result--title--title content--text-wrap"]').text
        date = cell.find_element(By.CSS_SELECTOR, '[class="ps-patent-result--title--ctr-pubdate"]').text
        ipcspan = cell.find_element(By.CSS_SELECTOR, '[class="ps-field ps-field--is-layout--inline "]')
        ipc = ipcspan.find_elements(By.TAG_NAME, 'span')[1].text
        application = cell.find_element(By.CSS_SELECTOR, '[class="ps-field--value notranslate"]').text
        applicant = cell.find_element(By.CSS_SELECTOR, '[class="ps-field--value ps-patent-result--applicant notranslate"]').text
        inventor = cell.find_element(By.CSS_SELECTOR, '[class="ps-field--value ps-patent-result--inventor notranslate"]').text
        patent = cell.find_element(By.CSS_SELECTOR, '[class="ui-outputpanel ui-widget ps-patent-result--abstract"]').text
        results.append({
            'publication number': pubnum,
            'name': name,
            'date of publication': date,
            'ipc': ipc,
            'application number': application,
            'applicant': applicant,
            'inventor': inventor,
            'patent': patent
        })
        """for t in results:
        print(c)
        for j in keys:
            print(f'{j}:{t[j]}')
        print('\n')"""
        c += 1
    print(f"{i+1} завершено")
    driver.find_element(By.CSS_SELECTOR, '[class="ui-commandlink ui-widget ps-link--has-icon js-paginator-next"]').click()
    WebDriverWait(driver, 10).until(
        text_to_be_present_in_element((By.CSS_SELECTOR, '[id="resultListForm:pageNumber"]'), f'{i+2}')
    )
    driver.refresh()

df = pd.DataFrame(results)
df.to_csv(r"../data/french-patents.csv")

driver.close()
