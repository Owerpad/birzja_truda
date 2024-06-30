import requests
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

def get_vacancies(page=0):
    url = 'https://api.hh.ru/vacancies'
    params = {
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
            'з/п': salary
        })
    
    return vacancies

all_vacancies = []
for page in range(5):
    all_vacancies.extend(get_vacancies(page))

df = pd.DataFrame(all_vacancies)

@app.route('/')
def index():
    sort_by = request.args.get('sort_by', 'должность')
    ascending = request.args.get('ascending', 'true') == 'true'
    search_query = request.args.get('search', '')

    filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
    sorted_df = filtered_df.sort_values(by=sort_by, ascending=ascending)

    return render_template('index.html', tables=[sorted_df.to_html(classes='data', header="true", index=False)], sort_by=sort_by, ascending=ascending, search_query=search_query)

if __name__ == '__main__':
    app.run(debug=True)
