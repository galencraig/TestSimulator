import fitz

# Function to extract content from PDF (both text and images)
def extract_content_from_pdf(pdf_path):
    content = []
    with fitz.open(pdf_path) as pdf_document:
        for page_number in range(len(pdf_document)):
            page = pdf_document.load_page(page_number)
            # Extract text
            text = page.get_text()
            content.append(text)
            # Extract images
            images = page.get_images(full=True)
            for img_index, img_info in enumerate(images):
                base_image = pdf_document.extract_image(img_info[0])
                image_bytes = base_image["image"]
                content.append(image_bytes)  # Store image bytes
    return content

# Function to parse question-answer pairs
def parse_questions(content):
    questions = []
    for item in content:
        if isinstance(item, str):
            lines = item.split("\n")
            question = ""
            answer_choices = []
            correct_answers = ""
            for line in lines:
                if line.startswith("Question #"):
                    if question:
                        questions.append((question, answer_choices, correct_answers))
                    question = line
                    answer_choices = []
                    correct_answers = ""
                elif line.startswith("Correct Answer:"):
                    correct_answers = line.split(":")[1].strip()
                elif line.startswith("A.") or line.startswith("B.") or line.startswith("C.") or line.startswith("D.") or line.startswith("E."):
                    answer_choices.append(line)
            # Append the last question
            if question:
                questions.append((question, answer_choices, correct_answers))
    return questions

# Function to present questions and collect answers
def take_test(questions):
    correct = 0
    total = len(questions)
    for question, answer_choices, correct_answers in questions:
        print(question)
        for choice in answer_choices:
            print(choice)
        answer = input("Your answer (e.g., 'ABCD'): ").upper()
        if answer == correct_answers:
            print("Correct!\n")
            correct += 1
        else:
            print("Incorrect. The correct answer(s) is/are:", correct_answers, "\n")
    print("You got {}/{} questions correct.".format(correct, total))

# Main function
def main():
    pdf_path = input("Enter the path of the PDF file: ")
    content = extract_content_from_pdf(pdf_path)  # Extract content (both text and images) from the PDF file
    questions = parse_questions(content)
    take_test(questions)

if __name__ == "__main__":
    main()



#from PyPDF2 import PdfReader
#
## Function to extract text from PDF
#def extract_text_from_pdf(pdf_path):
#    text = ""
#    with open(pdf_path, "rb") as f:
#        reader = PdfReader(f)
#        for page_num in range(len(pdf_reader.pages)):
#            page = pdf_reader.getPage(page_num)
#            text += page.extractText()
#    return text
#
## Function to parse question-answer pairs
#def parse_questions(text):
#    questions = []
#    lines = text.split("\n")
#    question = ""
#    answer_choices = []
#    correct_answers = []
#    for line in lines:
#        if line.startswith("Question #"):
#            if question:
#                questions.append((question, answer_choices, correct_answers))
#           question = line
#            answer_choices = []
#            correct_answers = []
#        elif line.startswith("Correct Answer:"):
#            correct_answers = line.split(":")[1].strip()
#        elif line.startswith("A.") or line.startswith("B.") or line.startswith("C.") or line.startswith("D.") or line.startswith("E."):
#            answer_choices.append(line)
#    # Append the last question
#    if question:
#        questions.append((question, answer_choices, correct_answers))
#    return questions
#
## Function to present questions and collect answers
#def take_test(questions):
#    correct = 0
#    total = len(questions)
#    for question, answer_choices, correct_answers in questions:
#        print(question)
#        for choice in answer_choices:
#            print(choice)
#        answer = input("Your answer (e.g., 'ABCD'): ").upper()
#        if answer == correct_answers:
#            print("Correct!\n")
#            correct += 1
#        else:
#            print("Incorrect. The correct answer(s) is/are:", correct_answers, "\n")
#    print("You got {}/{} questions correct.".format(correct, total))
#
## Main function
#def main():
#    pdf_path = input("Enter the path of the PDF file: ") 
#    text = extract_text_from_pdf(pdf_path)
#    questions = parse_questions(text)
#    take_test(questions)
#
#if __name__ == "__main__":
#    main()
