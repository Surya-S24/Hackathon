# Newsletter Filter and Recommendation System

## Overview
This project is designed for sales teams or individuals who regularly consume articles from e-newsletters. Traditional newsletters often contain a large amount of irrelevant information. To address this, our solution uses machine learning to scrape websites for content that aligns with user-provided keywords. Over time, the model learns user preferences through repeated keyword searches and displays personalized content recommendations.

## Features
1. **Keyword-Based Filtering**:
   - Users can input a newsletter article link and specify keywords.
   - The system fetches links to content relevant to the provided keywords.

2. **Machine Learning Integration**:
   - The model learns user preferences by analyzing keyword patterns.
   - Recommends content directly on the homepage based on past searches.

3. **Simplified Interface**:
   - A user-friendly web interface for inputting newsletter links and keywords.
   - Results are displayed in an organized and accessible manner.

## How It Works
1. **Input**:
   - Users provide a link to the newsletter article.
   - Keywords are entered into a dedicated input field.

2. **Processing**:
   - The model scrapes the provided website for content.
   - Keywords are matched with similar content in the newsletter.
   - Machine learning analyzes user search behavior for personalized recommendations.

3. **Output**:
   - Displays a list of top links related to the keyword.
   - Provides personalized content on the homepage based on frequently searched keywords.

## Technology Stack
- **Frontend**: [EJS,CSS,JS]
- **Backend**: [Python, Flask, BeautifulSoup, Pandas]
- **Web Scraping**: [BeautifulSoup]

## Future Scope
- Enhance the machine learning model for deeper personalization.
- Expand scraping capabilities to include multimedia content.
- Implement user authentication for secure and private recommendations.

## Images
![image](https://github.com/user-attachments/assets/fb0b6114-a36b-4bb6-9fa6-68967ec851b6)

![image](https://github.com/user-attachments/assets/cad73650-bfd9-41be-a7b9-83cd12d9bc71)

![image](https://github.com/user-attachments/assets/a6d13dc6-b98c-4ccf-ac6c-7454834cb3f6)

![image](https://github.com/user-attachments/assets/0d243019-5192-47f9-ae34-a41554145c2d)

## Contributing
We welcome contributions to improve this project. Please feel free to submit issues or pull requests.
