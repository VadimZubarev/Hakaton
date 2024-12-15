import db_data_search, db_data_save_to_json

if __name__ == "__main__":
    base_url = 'https://www.equationsheet.com'
    page_links = []
    num_of_formulas = 100

    for i in range(1, num_of_formulas+1):
        page_links.append(f'/eqninfo/Equation-{i:04}.html')

    latex_formulas = db_data_search.scrape_latex_from_site(base_url, page_links)
    db_data_save_to_json.save_formulas_to_json(latex_formulas)