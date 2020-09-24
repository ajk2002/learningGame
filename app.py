from questions import Question
question_prompts = [
    "5 + 5\n (a) 10\n (b) 20\n (c) 30\n\n ",
    "17 + 6\n (a) 12\n (b) 21\n (c) 23\n\n ",
    "7 + 14\n (a) 21\n (b) 16\n (c) 236\n\n "

]

questions = [
    Question(question_prompts[0], "a"),
    Question(question_prompts[1], "c"),
    Question(question_prompts[2], "a")
]

def run_test(questions):
    score = 0
    for question in questions:
        answer = input(question.prompt)
        if answer == question.answer:
            score  += 1
    print("You got " + str(score) + "/" + str(len(questions))+ " correct")

run_test(questions)