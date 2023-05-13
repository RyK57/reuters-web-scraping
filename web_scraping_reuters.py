import requests
import csv

# Define the file path and fieldnames
csv_file = "reuters_scraped_data.csv"

url = "https://www.reuters.com/assets/jsonWireNews"

try:
    response = requests.get(url)
    response.raise_for_status()
    json_data = response.json()

    articles = json_data["headlines"]

    scraped_data = []
    for article in articles:
        data = {}
        data["Title"] = article["headline"]
        data["Link"] = "https://www.reuters.com" + article["url"]
        data["Summary"] = article.get("description", "No summary available.")
        scraped_data.append(data)

        # Make API request to the News API
        api_key = "96292b12914f44549b0b329d57d5813d"
        news_api_url = "https://newsapi.org/v2/everything"
        payload = {
            "apiKey": api_key,
            "q": article["headline"],
            "pageSize": 1,
            "language": "en",
            "sortBy": "publishedAt"
        }

        try:
            response = requests.get(news_api_url, params=payload)
            response.raise_for_status()  # Raises an exception for HTTP errors
            news_data = response.json()

            if news_data["articles"]:
                article_data = news_data["articles"][0]
                data["Description"] = article_data["description"]
                data["Source"] = article_data["source"]["name"]
            else:
                data["Description"] = "No description available."
                data["Source"] = "N/A"

        except requests.exceptions.RequestException as e:
            print("Error: Failed to make API request:", e)
            # Handle the error as desired, e.g., exit the loop or continue with default values

    # Write the data to the CSV file
    with open(csv_file, "w", newline="", encoding="utf-8") as file:
        fieldnames = ["Title", "Link", "Summary", "Description", "Source"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(scraped_data)

    print("Data scraped successfully and saved to", csv_file)

except requests.exceptions.RequestException as e:
    print("Error: Failed to retrieve data from the website:", e)
