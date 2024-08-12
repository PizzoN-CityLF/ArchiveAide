from transformers import BartTokenizer, BartForConditionalGeneration
import os


def progress_bar(current, total, bar_length=10):
    fraction = current / total

    arrow = int(fraction * bar_length - 1) * '-' + '>'
    padding = int(bar_length - len(arrow)) * ' '

    ending = '\n' if current == total else '\r'

    print(f'Summary Progress: [{arrow}{padding}] {int(fraction*100)}%', end=ending)

def generate_summary(text, tokenizer, model):
    inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs, max_length=200, min_length=100, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

def getDirs(root):
    dirs = []
    for dir in os.listdir(root + "/out"):
        if dir[-4:] != ".csv":
            for dir2 in os.listdir(root + "/out/" + dir):
                for dir3 in os.listdir(root + "/out/" + dir + "/" + dir2):
                    dirs.append(root + "/out/" + dir + "/" + dir2 + "/" + dir3)
    return dirs

def main(root):
    tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
    model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
    print("Summarizer Initialized")
    dirs = getDirs(root)
    total = len(dirs)
    for i, dir in enumerate(dirs):
        with open(dir + "/text.txt", 'r', encoding="utf-8") as f:
            with open(dir + "/summary.txt", "w", encoding="utf-8") as f2:
                f2.write(generate_summary(f.read(), tokenizer, model))
        progress_bar((i+1), total)