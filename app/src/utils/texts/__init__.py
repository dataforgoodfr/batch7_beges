import glob
import os

TEXTS = {}

dirname = os.path.dirname(__file__)
for filename in glob.glob(dirname + "/*.md"):
    text_id = os.path.splitext(os.path.basename(filename))[0]
    with open(filename) as file_id:
        markdown_text = file_id.read()
    TEXTS[text_id] = markdown_text
