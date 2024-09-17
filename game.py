#Imports
import pygame, sys
from pygame.locals import *
import json
import random


pygame.init()

with open('NewCity.json') as f:
    dict_questions = json.load(f)
    # print(dict_questions["questions"][0]["question"]["ask"])
  
curr_question = random.randrange(0, len(dict_questions["questions"])) + 1  
WIDTH = 600
HEIGHT = 800
LINE_HEIGHT = HEIGHT // 25
timer = pygame.time.Clock()
time_count = 0
line = 1
fps = 60
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('New City Catechism Game')
font = pygame.font.Font('freesansbold.ttf', 18)
font12 = pygame.font.Font('freesansbold.ttf', 12)
font15 = pygame.font.Font('freesansbold.ttf', 15)
font14 = pygame.font.Font('freesansbold.ttf', 14)
# game variables
bg = int(.95 * 255), int(.95 * 255), int(.95 * 255)
white = 'white'
gray = 'gray'
black = 'black'
red = 'red'
orange = 'orange'
yellow = 'yellow'
green = 'green'
blue = 'blue'
purple = 'purple'
check = False
answer_showing = False
end_time_count = 0

class MultiLine:
    def __init__(self, text, font, list_of_lines, width_to_work_with):
        self.text = text
        self.font = font
        self.list_of_lines = list_of_lines
        self.width_to_work_with = width_to_work_with
        
    def separate_into_lines(self):
        # get the width of a space        
        text_width, text_height = self.font.size(" ")
        space_width = text_width
        text_width, text_height = self.font.size(self.text)
        if text_width < self.width_to_work_with:
            # will all fit on one line
            self.list_of_lines.append(self.text)
            return
        # Won't all fit on one line.  Start at the current beginning and add words until 
        # reach the end of the line.  If I run out of words before I reach the end of the 
        # line, this is the last line.
        words = self.text.split()
        current_line_nbr = 0
        current_word_nbr = 0
        current_line_text_width = 0
        current_line_text = ""
        done = False
        while not done:
            # check that no word by itself is wider than the width.  If it is, just quit.
            text_width, text_height = self.font.size(words[current_word_nbr])
            if text_width > self.width_to_work_with:
                words[current_word_nbr] = "Won't fit problem"
                return
            current_line_text_width = current_line_text_width + text_width + space_width
            # check to see if my current line text width is too big now
            if current_line_text_width >= self.width_to_work_with:
                # Yes, this is too much.  Quit with the previous word. 
                current_line_text_width = current_line_text_width - text_width
                self.list_of_lines.append(current_line_text)
                current_line_nbr = current_line_nbr + 1
                current_line_text = ""
                current_line_text_width = 0
            else:
                # There is still room on this line for more words
                if current_line_text == "":
                    current_line_text = current_line_text + words[current_word_nbr]
                else:
                    current_line_text = current_line_text + " " + words[current_word_nbr]
                current_word_nbr = current_word_nbr + 1
                # Are there any words left?
                if (current_word_nbr == len(words)):
                    done = True
                    if current_line_text != "":
                        self.list_of_lines.append(current_line_text)
    

# class for Buttons
class Button:
    def __init__(self, text, coords, size):
        self.text = text
        self.coords = coords
        self.size = size
        self.rect = pygame.rect.Rect(self.coords, self.size)

    def draw(self):
        if self.rect.collidepoint(mouse_coords) and mouse_buttons[0]:
            color = 'light blue'
        elif self.rect.collidepoint(mouse_coords):
            color = 'light gray'
        else:
            color = 'dark gray'
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, black, self.rect, 1)
        screen.blit(font.render(self.text, True, black),
                    (self.coords[0] + self.size[0] / 4, self.coords[1] + self.size[1] / 3))



# class for WordRectangles
class WordRectangle:
    def __init__(self, text, coords_orig, size, fontx):
        self.text = text
        self.coords = coords_orig
        self.size = size
        self.rect = pygame.rect.Rect(self.coords, self.size)
        self.fontx = fontx
        x, y = self.coords
        w, h = self.size
        self.rect2 = pygame.rect.Rect((x - 3, y - 3), (w + 3, h + 3))
        
    def get_coords(self):
        return self.coords
        
    def get_size(self):
        return self.size
        
    def set_coords(self, coords):
        self.coords = coords
        x, y = self.coords
        w, h = self.size
        if self.fontx == font15:
            self.rect2 = pygame.rect.Rect((x - 3, y - 3), (w + 3, h + 3))
        else:
            self.rect2 = pygame.rect.Rect((x - 2, y - 2), (w + 2, h + 2))
            
        
    def set_font(self, fontx):
        self.fontx = fontx

    def draw(self):
        if self.rect.collidepoint(mouse_coords) and mouse_buttons[0]:
            color = 'light blue'
        elif self.rect.collidepoint(mouse_coords):
            color = 'gray'
        else:
            color = 'black'
        pygame.draw.rect(screen, red, self.rect2, 1)
        screen.blit(self.fontx.render(self.text, True, color), self.coords)


class WordRecs:
    def __init__(self, orig_text):
        global line
        self.orig_text = orig_text
        self.orig_line_list = []
        multi_line = MultiLine(self.orig_text, font15, self.orig_line_list, WIDTH - 75)
        multi_line.separate_into_lines()
    # for i in range(len(lines_answer)):
    #     screen.blit(font12.render(lines_answer[i], True, black), (50, line * LINE_HEIGHT))
    #     line = line + 1    
        self.orig_word_list = self.orig_text.split()
        self.shuffled_word_list = self.orig_word_list
        random.shuffle(self.shuffled_word_list)
        self.bottom_wr_list = []
        self.top_wr_list = []
        self.prev_size = 40
        self.line_temp = 4
        line = 4
        coords = (10, (line + len(self.orig_line_list)) * LINE_HEIGHT)
        for i in range(len(self.shuffled_word_list)):
            text_width, text_height = font15.size(self.shuffled_word_list[i])
            self.bottom_wr_list.append(WordRectangle(self.shuffled_word_list[i], 
                            coords, (text_width + 3, text_height + 3), font15))
            coords = (coords[0] + text_width + 15, coords[1])
            if coords[0] > (WIDTH - 30):
                line = line + 1
                coords = (10, (line + len(self.orig_line_list)) * LINE_HEIGHT)
        
    def bottom_collidepoint(self, pos):
        for i in range(len(self.bottom_wr_list)):
            if self.bottom_wr_list[i].rect.collidepoint(pos):
                return (True, i)
        
    def top_collidepoint(self, pos):
        for i in range(len(self.top_wr_list)):
            if self.top_wr_list[i].rect.collidepoint(pos):
                return (True, i)
    
    def move_bottom_rec_to_top(self, i):
        coords = (0, 0)
        for j in range(len(self.top_wr_list)):
            coords = self.top_wr_list[j].get_coords()
        if coords == (0, 0):
            coords = (50, self.line_temp * LINE_HEIGHT)
        else:
            size = self.bottom_wr_list[i].get_size()
            coords = (coords[0] + self.prev_size + 2, coords[1])
            self.prev_size = size[0]
            if (coords[0] > (WIDTH - 75)):
                self.line_temp = self.line_temp + 1
                coords = (50, self.line_temp * LINE_HEIGHT)
            
        self.bottom_wr_list[i].set_coords(coords)
        self.bottom_wr_list[i].set_font(font14)
        self.top_wr_list.append(self.bottom_wr_list[i])
        self.bottom_wr_list.pop(i)
        self.draw()
        
    def draw(self):
        # draw the lines where the guesses will be put
        line = 4
        str_underlines = "___________________________________________________"
        for i in range(len(self.orig_line_list)):
            screen.blit(font.render(str_underlines, True, black),
                        (50, line * LINE_HEIGHT))
            line = line + 1

        line = line + 1
        for i in range(len(self.bottom_wr_list)):
            self.bottom_wr_list[i].draw()
        for i in range(len(self.top_wr_list)):
            self.top_wr_list[i].draw()
        
        line = line + len(self.orig_line_list) + 1
        if answer_showing:
            for i in range(len(self.orig_line_list)):
                screen.blit(font15.render(self.orig_line_list[i], True, black),
                            (50, line * LINE_HEIGHT))
                line = line + 1
        else:
            for i in range(len(self.orig_line_list)):
                screen.blit(font15.render("                                                      ", 
                            True, black),
                            (50, line * LINE_HEIGHT))
                line = line + 1
                
        
# draw the screen components
def draw_screen():
    global line
    # draw the information for the current question
    line = 1
    curr_question_text = "Question " + str(curr_question + 1)
    screen.blit(font.render(curr_question_text, True, black),
                (50, line * LINE_HEIGHT))
    line = line + 1
    lines = []
    multi_line = MultiLine(dict_questions["questions"][curr_question]["question"]["ask"], 
                            font, lines, WIDTH - 50)
    multi_line.separate_into_lines()
    for i in range(len(lines)):
        screen.blit(font.render(lines[i], True, black), (50, line * LINE_HEIGHT))
        line = line + 1
    wordRecs.draw()
    # buttons 
    submit_btn.draw()
    next_quest_btn.draw()
    quit_btn.draw()


        

#Game Loop
run = True
rectangle_dragging = False
wordRecs = WordRecs(dict_questions["questions"][curr_question]["question"]["answer"])
submit_btn = Button('Submit', (0, 19 * HEIGHT / 20), (WIDTH / 3, HEIGHT / 20))
next_quest_btn = Button('Next Question', (WIDTH / 3, 19 * HEIGHT / 20), (WIDTH / 3, HEIGHT / 20))
quit_btn = Button('Quit', (2 * (WIDTH / 3), 19 * HEIGHT / 20), (WIDTH / 3, HEIGHT / 20))

while run:
    timer.tick(fps)
    screen.fill(bg)
    mouse_coords = pygame.mouse.get_pos()
    mouse_buttons = pygame.mouse.get_pressed()
    draw_screen()
    time_count = time_count + 1
    if not answer_showing and (time_count % 500) == 0:
        end_time_count = time_count + 500
        answer_showing = True
    elif answer_showing and time_count >= end_time_count:
        answer_showing = False
      
    #Cycles through all events occuring  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if quit_btn.rect.collidepoint(event.pos):
                run = False
            elif next_quest_btn.rect.collidepoint(event.pos):
                curr_question = curr_question + 1
                if curr_question == len(dict_questions["questions"]):
                    curr_question = 0
                wordRecs = WordRecs(dict_questions["questions"][curr_question]["question"]["answer"])
            elif submit_btn.rect.collidepoint(event.pos):
                pass 
            else:
                try:
                    (bottom_collide, wordRec_index) = wordRecs.bottom_collidepoint(event.pos)
                    if bottom_collide:
                        wordRecs.move_bottom_rec_to_top(wordRec_index)
                except:
                    pass

    pygame.display.flip()
pygame.quit()