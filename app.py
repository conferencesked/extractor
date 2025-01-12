from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import spacy

# Initialize FastAPI app
app = FastAPI()

# Load an NLP model (spaCy)
nlp = spacy.load("en_core_web_sm")  # Use a language model like spaCy

# Define a data model for the API request
class URLRequest(BaseModel):
    url: str

# Route to extract event data
@app.post("/extract")
async def extract_event_data(request: URLRequest):
    try:
        # Step 1: Fetch the webpage content
        response = requests.get(request.url, timeout=10)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Unable to fetch URL content.")
        
        html_content = response.text
        
        # Step 2: Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")
        data = {}

        # Extract Title
        data['title'] = soup.title.string if soup.title else "N/A"
        
        # Extract Meta Description
        description_tag = soup.find("meta", attrs={"name": "description"})
        data['description'] = description_tag["content"] if description_tag else "N/A"

        # Step 3: NLP Analysis (extract entities)
        doc = nlp(html_content)
        data['entities'] = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]

        # Example for extracting dates and event-related info
        data['dates'] = [ent.text for ent in doc.ents if ent.label_ == "DATE"]
        data['locations'] = [ent.text for ent in doc.ents if ent.label_ == "GPE"]  # GPE = Geo-Political Entity (countries, cities)

        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
