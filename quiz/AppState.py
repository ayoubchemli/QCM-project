class AppState():

    def setStacked_widget(self, stacked_widget):
        self.stacked_widget = stacked_widget

    def setFullname(self, name):
        self.name = name
    
    def setEmail(self, email):
        self.email = email

    def setUsername(self, username):
        self.username = username
    
    def setPassword(self, password):
        self.password = password

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