from flask import Flask, render_template, request
import pandas as pd
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from io import BytesIO
import base64
app = Flask(__name__)
data = pd.read_csv("dantri_articles.csv")

data['Publish Time'] = data['Publish Time'].replace('Unknown', 'Sunday, 01/01/1900 - 00:00')
data['Publish Time'] = pd.to_datetime(data['Publish Time'], format='%A, %d/%m/%Y - %H:%M', errors='coerce')
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
    
    # Lấy 10 bài báo gần nhất
    latest_articles = data.sort_values(by='Publish Time', ascending=False).head(10)
    #Lấy thể loại
    categories = data['Category'].unique().tolist()


    return render_template('index.html', data=current_page_data, latest_articles=latest_articles, page_number=page_number, pagination_range=pagination_range, show_next_button=show_next_button,categories=categories)


df = pd.read_csv('dantri_articles.csv')
df['Combined'] = df[['Title', 'Content', 'Link', 'Image', 'Category', 'Author', 'Author Image', 'Publish Time', 'Author Link', 'Article Content']].apply(lambda x: ' '.join(x.astype(str)), axis=1)
@app.route('/search_results', methods=['POST'])
def search_query():
    search_query = request.form['search_query']
    # Filter DataFrame based on search query
    search_results = df[df['Combined'].str.contains(search_query, case=False)]
    num_results = len(search_results)  # Count the number of search results
    categories = data['Category'].unique().tolist() 
    
    return render_template('search_results.html', search_results=search_results, num_results=num_results,categories=categories)

@app.route('/article/<int:index>')
def article_detail(index):
    # Lấy thông tin của bài viết từ DataFrame sử dụng chỉ mục index
    article = df.loc[index]
    categories = data['Category'].unique().tolist()
    return render_template('article_detail.html', article=article,categories=categories)
    
    
@app.route('/thongke')
def thongke():
    # Thống kê số lượng bài báo theo thể loại
    category_counts = data['Category'].value_counts()

    # Vẽ biểu đồ tròn
    plt.figure(figsize=(8, 8))
    plt.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title('Thống kê thể loại bài báo chủ đề xã hội')
    
    # Lưu biểu đồ vào một đối tượng BytesIO để chuyển đổi thành định dạng base64
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    categories = data['Category'].unique().tolist()
    return render_template('thongke.html', plot_url=plot_url,categories=categories)


@app.route('/category/<category>')
def get_articles_by_category(category):
    articles = df[df['Category'] == category]
    categories = data['Category'].unique().tolist()
    category=category
    return render_template('theloai.html', articles=articles,categories=categories,category=category)

if __name__ == '__main__':
    app.run(debug=True)
