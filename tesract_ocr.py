from PIL import Image , ImageOps
import pytesseract
pngs=["/home/parthak/Videos/jev/Screenshot from 2026-09-25 23-14-07.png","/home/parthak/Videos/jev/Screenshot from 2026-09-26 02-25-44.png",
    "/home/parthak/Videos/jev/Screenshot from 2026-09-26 02-26-02.png","/home/parthak/Videos/jev/Screenshot from 2026-09-26 02-26-14.png",
    "/home/parthak/Videos/jev/Screenshot from 2026-09-26 02-26-14 copy.png","/home/parthak/Videos/jev/Screenshot from 2026-09-26 02-26-34.png"]
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

    print(f"\n--- {p.split('/')[-1]} ---")
    print(page_text[:200] if page_text.strip() else "⚠️  EMPTY - no text detected")
    text += page_text + "\n"

paper_text = text

if "Q1" not in paper_text and "Q.1" not in paper_text:
    print("Cannot read Q1 in the document!")
else:
    print("Q1 detected")
