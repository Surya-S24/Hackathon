from flask import Flask, request, render_template, jsonify
import requests
from bs4 import BeautifulSoup
import pandas as pd

app = Flask(__name__)

# In-memory list to store past searches
past_keywords = []

# Function to score headlines based on keywords
def score_headline(headline, keywords):
    return sum(keyword.lower() in headline.lower() for keyword in keywords)

@app.route('/', methods=['POST'])
def index():
    top_links = []
    suggested_keywords = list(set(past_keywords))  # Remove duplicates

    try:
        # Ensure the request is coming with the correct content type
        if request.content_type != 'application/x-www-form-urlencoded':
            return jsonify({'error': 'Invalid content type'}), 400

        url = request.form['website_url']
        interest_keywords_str = request.form['interest_keyword']

        # Update past keywords list
        new_keywords = [keyword.strip() for keyword in interest_keywords_str.split(',')]
        past_keywords.extend(new_keywords)

        # Split the interest keywords by commas and strip extra whitespace
        interest_keywords = [keyword.strip() for keyword in interest_keywords_str.split(',')]

        # Send an HTTP GET request to the URL
        response = requests.get(url)

        if response.status_code == 200:
            # Parse the page content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all <span> tags with class 'post-title'
            spans = soup.find_all('span', class_='post-title')

            # Initialize lists to store text and links
            span_texts = []
            links = []

            for span in spans:
                # Find the parent <a> tag, assuming it's a direct parent or nearby
                parent_a = span.find_parent('a')
                if parent_a and parent_a.has_attr('href'):
                    # Extract the text and href
                    span_texts.append(span.get_text(strip=True))
                    links.append(parent_a['href'])

            # Score headlines based on interest keywords
            interest_scores = [score_headline(h, interest_keywords) for h in span_texts]

            # Create a DataFrame with headlines, links, and their scores
            df = pd.DataFrame({
                'Headline': span_texts,
                'Link': links,
                'Interest Score': interest_scores
            })

            # Sort headlines by the interest score in descending order
            sorted_df = df.sort_values(by='Interest Score', ascending=False)

            # Get top 5 links
            top_links = sorted_df.head(5).to_dict(orient='records')
        else:
            top_links = [{'Headline': 'Error', 'Link': '', 'Interest Score': 0}]
    except KeyError as e:
        return jsonify({'error': f'Missing field: {e}'}), 400
    except Exception as e:
        return jsonify({'error': f'An error occurred: {e}'}), 500

    return jsonify({'top_links': top_links, 'suggested_keywords': suggested_keywords})

@app.route('/add_suggestion', methods=['POST'])
def add_suggestion():
    try:
        keyword = request.json.get('keyword')
        if keyword and keyword not in past_keywords:
            past_keywords.append(keyword)
        return jsonify({'status': 'success', 'suggested_keywords': list(set(past_keywords))})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=8000)
