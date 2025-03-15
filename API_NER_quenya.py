from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
import spacy

"""
Lancer l'API dans Uvicorn : 

uvicorn API_NER_quenya:app

puis aller à http://localhost:8000/front/quenya.html
"""

app = FastAPI()

# Gestion des pages locales
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/front", StaticFiles(directory="web"), name="front")


class InputData(BaseModel):
    sentence: str


@app.post("/ner_quenya")
async def postag(inpt: InputData, model="spacy/models/balanced_fin_false_0.01_1000/model-best"):
    nlp = spacy.load(model)
    doc = nlp(inpt.sentence)

    lst = "\n".join([f"<li>{entity.text}: {entity.label_}</li>" for entity in doc.ents])
    starts = [entity.start_char for entity in doc.ents]
    ends = [entity.end_char for entity in doc.ents]
    labels = [entity.label_ for entity in doc.ents]
    txt = "<p>"
    for index, char in enumerate(doc.text):
        if index in starts:
            nb = starts.index(index)
            label = "person"
            if labels[nb] == "LOC":
                label = "location"
            txt = txt + f"<span class={label}>" + char
        elif index in ends:
            txt = txt + char + "</span>"
        else:
            txt = txt + char
    txt = txt + "</p>" "\n" + "<p><span class=person> PERSON <span>" + "&nbsp;&nbsp;&nbsp;&nbsp;" + "<span class=location> LOCATION <span></p>"

    html_content = f"<h1>RESULTATS:</h1>\n<ol>\n{lst}</ol> \n {txt}"
    return HTMLResponse(content=html_content, status_code=200)