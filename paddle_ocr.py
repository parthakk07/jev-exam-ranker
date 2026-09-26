from paddleocr import PaddleOCR

pngs = [
    "/home/parthak/Videos/jev/Screenshot from 2026-09-25 23-14-07.png",
    "/home/parthak/Videos/jev/Screenshot from 2026-09-26 02-25-44.png",
    "/home/parthak/Videos/jev/Screenshot from 2026-09-26 02-26-02.png",
    "/home/parthak/Videos/jev/Screenshot from 2026-09-26 02-26-14.png",
    "/home/parthak/Videos/jev/Screenshot from 2026-09-26 02-26-14 copy.png",
    "/home/parthak/Videos/jev/Screenshot from 2026-09-26 02-26-34.png",
]
ocr = PaddleOCR(lang="en", enable_mkldnn=False)

text = ""
for p in pngs:
    if "copy" in p.lower():
        continue
    result = ocr.predict(p)
    page_lines = result[0]["rec_texts"]
    page_text = "\n".join(page_lines)

    print(f"\n--- {p.split('/')[-1]} ---")
    print(page_text[:300] if page_text.strip() else "⚠️  EMPTY")

    text += page_text + "\n"

paper_text = text
print("\n--- FULL PREVIEW ---")
print(paper_text[:300])
print("---------------\n")

if "Q1" in paper_text or "Q.1" in paper_text or "Q. No. 1" in paper_text or "Question 1" in paper_text:
    print("Success! Q1 detected")
else:
    print("stop: Cannot read Q1")
