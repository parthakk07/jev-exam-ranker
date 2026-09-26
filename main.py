import os
from dotenv import load_dotenv
from typesafe_sdk import Choice, Noul, Score, TypeSafeClient
from PIL import Image , ImageOps
import pytesseract

pngs = []
while True:
    t = input("enter the image path (n for exit): ").strip()
    if t.lower() == "n":
        break
    if t:
        pngs.append(t)

config = "--oem 1 --psm 6"
text=""
for p in pngs:
    if "copy" in p.lower() :
        continue
    image = Image.open(p)
    image=ImageOps.grayscale(image)
    image = ImageOps.autocontrast(image)
    image= image.resize((image.width *2 , image.height *2 ),Image.Resampling.LANCZOS)
    page_text = pytesseract.image_to_string(image, lang="eng", config=config)

    text += page_text + "\n"

paper_text = text

if len(paper_text.strip()) < 80:
    raise SystemExit("OCR too empty — fix images before calling Jev")
load_dotenv()

api_key = os.getenv("JEV_API_KEY")
if not api_key:
    raise ValueError(" API key not found in .env file!")

topics = [t.strip() for t in input("topics > ").split(",") if t.strip()]

questions = {}
for topic in topics:
    questions[f"{topic}__present"] = Noul(
        instructions=f"Is the topic '{topic}' present anywhere in this exam paper?",
    )
    questions[topic] = Score(
        instructions=f"How strongly is '{topic}' emphasized in this exam paper?",
        criteria=[
            "Not covered at all in this paper",
            "Covered briefly, as a minor part of one question",
            "Covered heavily, with multiple or high-mark questions on it",
        ],
    )
state = {"kind": "exam paper", "text": paper_text}

try:
    with TypeSafeClient(api_key=api_key) as client:
        response = client.system_one(state=state, questions=questions)
except Exception as e:
    raise SystemExit(f"TypeSafe API error: {e}") from e

scored=[]
for topic in topics :
    present = response.nouls[f"{topic}__present"].noul
    ans=response.scores[topic]
    scored.append((topic,present,ans.score,ans.probabilities))

scored.sort(key=lambda x: x[2], reverse=True)

print("X--x--X--x--X--x--X--x--X--x--X--x")
print()

for topic, present, score, probs in scored:
    print(f"{topic.strip()}  present={present:.2f}  score={score:.2f}  {probs}")
