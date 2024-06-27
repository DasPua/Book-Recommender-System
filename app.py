from flask import Flask, redirect, url_for, render_template, request
import pickle as pkl
import numpy as np

books = pkl.load(open('books.pkl', 'rb'))
pt = pkl.load(open('pt.pkl', 'rb'))
cosine_sim_matrix = pkl.load(open('cosine_sim_matrix.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('listings/login.html')

@app.route('/signup')
def signup():
    return render_template('listings/signup.html')

@app.route('/listings')
def all_listings():
    user_input = "1984"
    
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(cosine_sim_matrix[index])), key=lambda x: x[1], reverse=True)[:50]
    data = []

    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)

        print(pt.index[i[0]])
    
    return render_template('listings/index.html', allListings=data)

@app.route('/recommend')
def recommend_page():
    return render_template('listings/recommends.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    user_input = request.form.get('title')
    
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(cosine_sim_matrix[index])), key=lambda x: x[1], reverse=True)[:50]
    data = []

    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)

        print(pt.index[i[0]])

    return show_results(data)

@app.route('/listing')
def show_results(data):
    return render_template('listings/show.html', listings=data)

if __name__ == '__main__':
    app.run(debug=True)
