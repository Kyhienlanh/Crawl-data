from flask import Flask, render_template, request
import pandas as pd
import csv
app = Flask(__name__)
data = pd.read_csv("dantri_articles.csv")
# Pagination function
def paginate(page_number, per_page):
    start = (page_number - 1) * per_page
    end = start + per_page
    return data[start:end]

@app.route('/')
def index():
    page_number = int(request.args.get('page', 1))
    per_page = 13
    total_pages = (data.shape[0] - 1) // per_page + 1
    start_page = max(1, page_number - 2)
    end_page = min(start_page + 4, total_pages)
    if end_page - start_page < 4:
        start_page = max(1, end_page - 4)
    pagination_range = range(start_page, end_page + 1)
    show_next_button = page_number < total_pages
    current_page_data = paginate(page_number, per_page)
    return render_template('index.html', data=current_page_data, page_number=page_number, pagination_range=pagination_range, show_next_button=show_next_button)


df = pd.read_csv('dantri_articles.csv')
df['Combined'] = df[['Title', 'Content', 'Link', 'Image', 'Category', 'Author', 'Author Image', 'Publish Time', 'Author Link', 'Article Content']].apply(lambda x: ' '.join(x.astype(str)), axis=1)
@app.route('/search_results', methods=['POST'])
def search_query():
    search_query = request.form['search_query']
    # Filter DataFrame based on search query
    search_results = df[df['Combined'].str.contains(search_query, case=False)]
    num_results = len(search_results)  # Count the number of search results
    return render_template('search_results.html', search_results=search_results, num_results=num_results)


@app.route('/article/<int:index>')
def article_detail(index):
    # Lấy thông tin của bài viết từ DataFrame sử dụng chỉ mục index
    article = df.loc[index]
    return render_template('article_detail.html', article=article)
    
if __name__ == '__main__':
    app.run(debug=True)
