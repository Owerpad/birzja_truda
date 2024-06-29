import requests
import pandas as pd

def get_vacancies(page=0):
    url = 'https://api.hh.ru/vacancies'
    params = {
        'text': 'Python',
        'area': 1,  # Москва
        'page': page,
        'per_page': 20
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    vacancies = []
    
    for item in data['items']:
        title = item['name']
        link = item['alternate_url']
        company = item['employer']['name']
        location = item['area']['name']
        
        salary = item.get('salary')
        if salary:
            if salary['from'] and salary['to']:
                salary = f"{salary['from']} - {salary['to']} {salary['currency']}"
            elif salary['from']:
                salary = f"от {salary['from']} {salary['currency']}"
            elif salary['to']:
                salary = f"до {salary['to']} {salary['currency']}"
        else:
            salary = 'Нет информации'
        
        vacancies.append({
            'должность': title,
            'ссылка': link,
            'работодатель': company,
            'регион': location,
            'з\п': salary
        })
    
    return vacancies

all_vacancies = []
for page in range(5):
    all_vacancies.extend(get_vacancies(page))

df = pd.DataFrame(all_vacancies)
print(df)
