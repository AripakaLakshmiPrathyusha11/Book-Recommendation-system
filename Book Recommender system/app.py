from flask import Flask,request,render_template,request
import pickle
import numpy as np

popularity_df = pickle.load(open('popularity_df.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
book = pickle.load(open('books.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')



@app.route('/books')
def books():
    return render_template('books.html',
                           book_name = list(popularity_df['Book-Title'].values),
                           author=list(popularity_df['Book-Author'].values),
                           image=list(popularity_df['Image-URL-M'].values),
                           votes=list(popularity_df['No.Of.Ratings'].values),
                           rating=list(popularity_df['AVG_Ratings'].values)
                           )



@app.route('/aboutme')
def aboutme():
    return render_template('aboutme.html')

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_name = request.form.get('user_name')
    index = np.where(pt.index == user_name)[0][0]
    similar_books = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1], reverse=True)[1:5]
    
    data = []
    for i in similar_books:
        item =[]
        temp_df = book[book['Book-Title']==pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        
        data.append(item)
    

    return render_template('recommend.html',data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)