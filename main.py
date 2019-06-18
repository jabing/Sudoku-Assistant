"""
Sudoku Assistant Features
=========================
    A Sudoku Practice and Answering Tool Application

    Target platform: Android, Win
    Dependent on kivy frame of python3

Author: Jiang JIaping
Data: 2019-06-08
"""

from kivy.app import App
from os.path import dirname, join
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, \
    ListProperty
from kivy.uix.screenmanager import Screen
from kivy.config import Config
from solution import Solution


Config.set('graphics', 'width', 460)
Config.set('graphics', 'height', 880)


class SdScreen(Screen):
    fullscreen = BooleanProperty(False)

    def add_widget(self, *args):
        if 'content' in self.ids:
            return self.ids.content.add_widget(*args)
        return super(SdScreen, self).add_widget(*args)


class SdzsApp(App):
    index = NumericProperty(-1)
    current_title = StringProperty()
    screen_names = ListProperty([])
    available_screens = []
    screens = {}
    # 6 Square Grid
    msg6 = StringProperty()
    back_rest_6 = StringProperty()
    board6 = ListProperty([])
    idx6 = NumericProperty(-1)
    font_color6 = ListProperty([])
    fg_color6 = ListProperty([])
    num_state6 = ListProperty([])
    sudo6 = None
    backup_6 = None
    # 9 Square Grid
    msg9 = StringProperty()
    back_rest_9 = StringProperty()
    board9 = ListProperty([])
    idx9 = -1
    sudo9 = None
    backup_9 = None
    font_color9 = ListProperty([])
    fg_color9 = ListProperty([])
    num_state9 = ListProperty([])
    def build(self):
        # 6 Square Grid
        self.click_reset_6()    # init all of cell on board
        # 9 Square Grid
        self.click_reset_9()    # init all of cell on board
        # Screen
        self.title = 'Sudoku Assistant v1.0'
        self.available_screens = sorted(['Square6', 'Square9', 'Home'])
        self.screen_names = self.available_screens
        self.available_screens = [join(dirname(__file__), 'data', 'screen','{}.kv'.format(fn).lower()) for fn in self.available_screens]
        self.go_next_screen()

    # Function for 6 Square Grid ---------------------------------------------------------
    def idx_to_pos_6(self, idx):
        return (idx // 6, idx % 6)

    def show_msg_6(self, msg):
        self.msg6 = "[color=fff333][b][i]" + msg + "[/i][/b][/color]"
    
    def click_num_6(self, num):
        self.msg6 = ''
        if num < 0 or self.idx6 < 0 \
                or self.board6[self.idx6] == num:
            return

        (row, col) = self.idx_to_pos_6(self.idx6)
        if self.sudo6.change_cell(row, col, num):
            self.board6[self.idx6] = num
            self.set_same_number_color_6(num)
            self.set_num_state_6()
        else:
            # self.board6[self.idx6] = num
            self.show_msg_6(str(num) + " is incorrect.")
            self.board6[self.idx6] = 0

    def click_cell_6(self, idx):
        self.idx6 = idx
        self.msg6 = ''
        self.reset_color_6()
        if idx >= 0:
            self.set_notice_area_color_6(idx)
            if self.board6[idx] > 0:
                self.set_same_number_color_6(self.board6[idx])

    def click_clear_6(self):
        self.msg6 = ''
        if -1 != self.idx6:
            self.board6[self.idx6] = 0
            (row, col) = self.idx_to_pos_6(self.idx6)
            self.sudo6.change_cell(row, col, 0)
            self.set_num_state_6()

    def reset_color_6(self):
        self.font_color6 = [(1, 1, 1, 1) for i in range(0, 36)]
        self.fg_color6 = [(0, 0, 0, 0) for i in range(0, 36)]

    def set_same_number_color_6(self, num):
        for i in range(0, 36):
            self.font_color6[i] = (1, 1, 0, 1) if num == self.board6[i] else (1, 1, 1, 1)
            # self.fg_color6[i] = (0, 1, 1, 0.1) if num == self.board6[i] else (1, 1, 1, 0)

    def set_notice_area_color_6(self, idx):
        # calculate which Square the cell is located
        row, col = self.idx_to_pos_6(idx)
        for i in range(0, 6):
            self.fg_color6[row * 6 + i] = (1, 0, 0, 0.2)
        for i in range(0, 6):
            x = i * 6 + col
            self.fg_color6[x] = (0 + self.fg_color6[x][0],
                                 1 + self.fg_color6[x][1],
                                 0 + self.fg_color6[x][2],
                                 0.2)
        row, col = row // 2 * 2, col // 3 * 3
        # get all cell of the Square
        for i in range(0, 3):
            x = row * 6 + col+i
            self.fg_color6[x] = (0 + self.fg_color6[x][0],
                                 0 + self.fg_color6[x][1],
                                 1 + self.fg_color6[x][2],
                                 0.2)
            y = (row + 1) * 6 + col + i
            self.fg_color6[y] = (0 + self.fg_color6[y][0],
                                 0 + self.fg_color6[y][1],
                                 1 + self.fg_color6[y][2],
                                 0.2)

    def set_num_state_6(self):
        num_count = [0 for i in range(0, 7)]
        for i in range(0, 36):
            num_count[self.board6[i]] += 1
        for i in range(1, 7):
            self.num_state6[i] = num_count[i] == 6

    def click_reset_6(self):
        self.back_rest_6 = "Save"
        self.show_msg_6('')
        self.board6 = [i*0 for i in range(0, 36)]
        self.num_state6 = [False for i in range(0, 7)]
        self.reset_color_6()
        self.sudo6 = Solution([
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ])

    def click_backup_6(self):
        self.msg6 = ''
        if self.back_rest_6 == "Save":
            self.backup_6 = self.board6[:]
            self.back_rest_6 = "Restore"
            self.show_msg_6('Saved, use RESTORE to call it back.')
        else:
            self.back_rest_6 = "Save"
            self.board6 = self.backup_6[:]
            for i in range(0, 36):
                r, c = self.idx_to_pos_6(i)
                self.sudo6.matrix[r][c] = self.board6[i]
            self.set_num_state_6()
            self.show_msg_6('Restored..')

    def click_answer_6(self):
        self.msg6 = ''
        if self.sudo6.solve():
            if self.back_rest_6 == "Save":
                self.click_backup_6()
            for i in range(0, 36):
                r,c = self.idx_to_pos_6(i)
                self.board6[i] = self.sudo6.matrix[r][c]
            self.show_msg_6('Answer')
            self.set_num_state_6()
        else:
            self.show_msg_6('No correct answer')

    # Function for 9 Square Grid  --------------------------------------------------
    def idx_to_pos_9(self, idx):
        return (idx // 9, idx % 9)

    def show_msg_9(self, msg):
        self.msg9 = "[color=fff333][b][i]" + msg + "[/i][/b][/color]"

    def reset_color_9(self):
        self.font_color9 = [(1, 1, 1, 1) for i in range(0, 81)]
        self.fg_color9 = [(0, 0, 0, 0) for i in range(0, 81)]

    def set_same_number_color_9(self, num):
        for i in range(0, 81):
            self.font_color9[i] = (1, 1, 0, 1) if num == self.board9[i] else (1, 1, 1, 1)
            # self.fg_color9[i] = (0, 1, 1, 0.1) if num == self.board9[i] else (1, 1, 1, 0)

    def set_notice_area_color_9(self, idx):
        # calculate which Square the cell is located
        row, col = self.idx_to_pos_9(idx)
        for i in range(0, 9):
            self.fg_color9[row * 9 + i] = (1, 0, 0, 0.2)
        for i in range(0, 9):
            x = i * 9 + col
            self.fg_color9[x] = (0 + self.fg_color9[x][0],
                                 1 + self.fg_color9[x][1],
                                 0 + self.fg_color9[x][2],
                                 0.2)
        row, col = row // 3 * 3, col // 3 * 3
        # get all cell of the Square
        for i in range(0, 3):
            x = row * 9 + col+i
            self.fg_color9[x] = (0 + self.fg_color9[x][0],
                                 0 + self.fg_color9[x][1],
                                 1 + self.fg_color9[x][2],
                                 0.2)
            y = (row + 1) * 9 + col + i
            self.fg_color9[y] = (0 + self.fg_color9[y][0],
                                 0 + self.fg_color9[y][1],
                                 1 + self.fg_color9[y][2],
                                 0.2)
            y = (row + 2) * 9 + col + i
            self.fg_color9[y] = (0 + self.fg_color9[y][0],
                                 0 + self.fg_color9[y][1],
                                 1 + self.fg_color9[y][2],
                                 0.2)

    def set_num_state_9(self):
        num_count = [0 for i in range(0, 10)]
        for i in range(0, 81):
            num_count[self.board9[i]] += 1
        for i in range(1, 10):
            self.num_state9[i] = num_count[i] == 9

    def click_num_9(self, num):
        self.msg9 = ''
        if num < 0 or self.idx9 < 0 \
                or self.board9[self.idx9] == num:
            return

        (row, col) = self.idx_to_pos_9(self.idx9)
        if self.sudo9.change_cell(row, col, num):
            self.board9[self.idx9] = num
            self.set_same_number_color_9(num)
            self.set_num_state_9()
        else:
            # self.board9[self.idx9] = num
            self.show_msg_9(str(num) + " is incorrect.")
            self.board9[self.idx9] = 0

    def click_cell_9(self, idx):
        self.idx9 = idx
        self.msg9 = ''
        self.reset_color_9()
        if idx > 0:
            self.set_notice_area_color_9(idx)
            if idx >= 0 and self.board9[idx] > 0:
                self.set_same_number_color_9(self.board9[idx])

    def click_clear_9(self):
        self.msg9 = ''
        if -1 != self.idx9:
            self.board9[self.idx9] = 0
            (row, col) = self.idx_to_pos_9(self.idx9)
            self.sudo9.change_cell(row, col, 0)
            self.set_num_state_9()

    def click_reset_9(self, *args):
        self.back_rest_9 = "Save"
        self.show_msg_9('')
        self.board9 = [0 for i in range(0, 81)]
        self.num_state9 = [False for i in range(0, 10)]
        self.reset_color_9()
        self.font_color9 = [(1, 1, 1, 1) for i in range(0, 81)]
        self.fg_color9 = [(1, 1, 1, 0) for i in range(0, 81)]
        self.sudo9 = Solution([
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ])

    def click_backup_9(self):
        self.msg9 = ''
        if self.back_rest_9 == "Save":
            self.backup_9 = self.board9[:]
            self.back_rest_9 = "Restore"
            self.show_msg_9('Saved, use RESTORE to call it back.')
        else:
            self.back_rest_9 = "Save"
            self.board9 = self.backup_9[:]
            for i in range(0, 81):
                r, c = self.idx_to_pos_9(i)
                self.sudo9.matrix[r][c] = self.board9[i]
            self.set_num_state_9()
            self.show_msg_9('Restored..')

    def click_answer_9(self):
        self.msg9 = ''
        if self.sudo9.solve():
            if self.back_rest_9 == "Save":
                self.click_backup_9()
            for i in range(0, 81):
                r, c = self.idx_to_pos_9(i)
                self.board9[i] = self.sudo9.matrix[r][c]
            self.show_msg_9('Answer')
            self.set_num_state_9()
        else:
            self.show_msg_9('No correct answer')

    # Screen -------------------------------------------------------------
    def on_pause(self):
        return True

    def on_resume(self):
        pass

    def on_current_title(self, instance, value):
        self.root.ids.spnr.text = value

    def go_previous_screen(self):
        self.index = (self.index - 1) % len(self.available_screens)
        screen = self.load_screen(self.index)
        sm = self.root.ids.sm
        sm.switch_to(screen, direction='right')
        self.current_title = screen.name

    def go_next_screen(self):
        self.index = (self.index + 1) % len(self.available_screens)
        screen = self.load_screen(self.index)
        sm = self.root.ids.sm
        sm.switch_to(screen, direction='left')
        self.current_title = screen.name

    def go_screen(self, idx):
        self.index = idx
        screen = self.load_screen(idx)
        self.root.ids.sm.switch_to(screen, direction='left')
        self.current_title = screen.name

    def load_screen(self, index):
        if index in self.screens:
            return self.screens[index]
        screen = Builder.load_file(self.available_screens[index])
        self.screens[index] = screen
        return screen


if __name__ == '__main__':
    SdzsApp().run()
