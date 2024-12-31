from data_handler import read_subjects,read_chapters

class Subject:
    def __init__(self, course,chapter_id,chapter_title):
        self.course = course
        self.chapter_id = chapter_id
        self.chapter_title = chapter_title


    def get_questions(self):
        all_chapters = Subject.get_all_chapters_of_course(self.course)
        chapter = all_chapters[self.chapter_id]

        questions = chapter['questions']
        return questions

    def to_dict(self):
        return {
            "course": self.course,
            "chapter_id": self.chapter_id,
            "chapter":self.chapter_title
        }

    ##udpos213
    @staticmethod
    def get_all_courses():
        return read_subjects()

    #udpos213
    @staticmethod
    def get_all_chapters_of_course(course):
        return read_chapters(course)

    #udpos213 toSHowHow to use Subject.get_all_courses()
    @staticmethod
    def print_all_subjects():
        subjects = Subject.get_all_courses()
        if not subjects:
            print("No subjects available.")
            return

        for subject in subjects:
            print(f"Title: {subject['title']}")
            print(f"Description: {subject['description']}")
            print(f"Chapters: {', '.join(subject['chapters'])}")
            print(f"Is New: {'Yes' if subject['is_new'] else 'No'}")
            print("-" * 40)

    # udpos213 toSHowHow to use Subject.get_all_chapters_of_course(course)
    @staticmethod
    def print_all_chapters_of_course(course):
        chapters = Subject.get_all_chapters_of_course(course)
        if not chapters:
            print("No chapters available.")
            return
        for chapter in chapters:
            print(f"Title: {chapter['title']}")
            print(f"Description: {chapter['description']}")
            print(f"questions_count: {chapter['questions_count']} question")
            print(f"time_estimate: {chapter['time_estimate']}")
            print(f"difficulty: {['difficulty']}")
            print(f"Is New: {'Yes' if chapter['is_new'] else 'No'}")
            print("-" * 40)


    @staticmethod
    def display_questions_in_coonsole(subject):
        for q in subject.get_questions():
            print(f"Question: {q['question']}")
            print(f"Answers: {q['answers']}")
            print(f"correctAnswer: {q['correctAnswer']}")

            print("-" * 40)



    # @staticmethod
    # def get_name_of_chapter(course,chapter_id):
    #     all_chapters = Subject.get_all_chapters_of_course(course)
    #     chapter = all_chapters[chapter_id]
    #     return chapter['title']



