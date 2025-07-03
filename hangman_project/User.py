class User:

    def __init__(self, user_name, identity_num, password):
        self.user_name = user_name
        self.identity_num = identity_num
        self.password = password
        self.play_times = 0
        self.word_list = []
        self.num_win = 0

    def __str__(self):
        # string =  "{"+f'"user_name": "{self.user_name}","password": "{self.password}","play_times": {self.play_times},"word_list": {self.word_list},"num_win": {self.num_win}'+'  }}'

        string = "{\n"+ f'    "user_name": "{self.user_name}",\n    "password": "{self.password}",\n    "play_times": {self.play_times},\n    "word_list": {self.word_list},\n    "num_win": {self.num_win}\n'+'  }\n}'
        return string
        # return ('\n user_name: "'+self.user_name+'",\n'
        # ' identity_num: "'+self.identity_num+'",\n'
        # ' password: "'+self.password+'",\n'
        # ' play_times: '+self.play_times+'",\n word_list: '+ self.word_list
        #     "": 321,
        #     "": 555,
        #     "play_times": 0,
        #     "word_list": [],
        #     "num_win": 0
        #
        # return f", user name: {self.user_name}, identity number: {self.identity_num}, password: {self.password}, play times: {self.play_times}, word list: {self.word_list}, num win: {self.num_win} ]"

