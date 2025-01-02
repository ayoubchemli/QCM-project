class AppState():

    def setUser(self, user):
        self.user = user

    def setCourse(self, course):
        self.course = course

    def setChapters(self, chapters):
        self.chapters = chapters

    def setChapterID(self, chapter_id):
        self.chapter_id = chapter_id

    def setQuestions(self, questions):
        self.questions = questions

    def setAnswers(self, answers):
        self.answers = answers

    def setTestInstance(self, test_instance):
        self.test_instance = test_instance

    def getTestInstance(self):
        return self.test_instance

    def getStacked_widget(self):
        return self.stacked_widget

    def getFullname(self):
        return self.name
    
    def getEmail(self):
        return self.email
    
    def getUsername(self):
        return self.username
    
    def getPassword(self):
        return self.password
    
    def getUser(self):
        return self.user

    def getCourse(self):
        return self.course

    def getChapters(self):
        return self.chapters

    def getChapterID(self):
        return self.chapter_id

    def getQuestions(self):
        return self.questions
    
    def getAnswers(self):
        return self.answers