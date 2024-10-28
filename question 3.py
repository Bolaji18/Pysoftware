import fitz  
from fakeModels import SubjectCategoryMapping, Subjects  
from .models import Question  
import re
from datetime import datetime


def parse_and_save_question(text):
    option_pattern = r"([A-E])\.\s(.+?)(?=(?:[A-E]\.|$))"
    
    question_part, *options_part = text.split('\n')
    options = re.findall(option_pattern, ' '.join(options_part))

    if not question_part or len(options) < 4:
        return

    
    option_dict = {'a': None, 'b': None, 'c': None, 'd': None, 'e': None}
    for i, (option_letter, option_text) in enumerate(options):
        if i < 5:
            option_dict[option_letter.lower()] = option_text.strip()

    category = SubjectCategoryMapping.objects.first()
    multiple_quiz_use_subject = Subjects.objects.all()[:1]  

    
    question_instance = Question.objects.create(
        category=category,
        question_main=question_part.strip(),
        question_severity="1",  
        question_preamble="Default preamble text",  
        question_set_by="Author Placeholder",  
        question_authorised_by="Authorized Placeholder",  
        year_of_past_question=datetime(1994, 1, 1),  
        a=option_dict['a'],
        b=option_dict['b'],
        c=option_dict['c'],
        d=option_dict['d'],
        e=option_dict['e'],
        hidden=False,  
        explanation="Default explanation" 
    )
    
    
    question_instance.multiple_quiz_use_subject.set(multiple_quiz_use_subject)


def extract_text_from_pdf(pdf_path):
    with fitz.open(pdf_path) as pdf:
        text = ""
        for page in pdf:
            text += page.get_text()
    return text

# Define main function to process PDF and save questions
def main():
    pdf_path = "Principles_of_Accounts_1994.pdf" 
    full_text = extract_text_from_pdf(pdf_path)
    question_blocks = re.split(r'\n\d+\.\s', full_text)[1:] 

    for block in question_blocks:
        parse_and_save_question(block)

# Run the main function
if __name__ == "__main__":
    main()
