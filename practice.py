
class people:

    def __init__(self, gender, head, body):
        """
        
        self 指向的是class本身
        """
        self.gender =gender
        self.head = head
        self.body = body

    def eat(self):

        self.head
        print("Now you are eating")
    
    def run(self):

        self.eat()
        print("after eating, you are running")