
import darkdetect
from PIL import Image
from configuration import *
import customtkinter as ctk

try:
    from ctypes import windll, byref, sizeof, c_int
except Exception as e:
    pass

class calc(ctk.CTk):
    def __init__(self,is_dark,):
        #root
        super().__init__(fg_color=(WHITE,BLACK))
        self.geometry(f'{APP_SIZE[0]}x{APP_SIZE[1]}')
        self.resizable(False,False)
        self.title('CALCULATOR')
        self.iconbitmap('img.ico')
      
        
        #title bar
        try:
            self.title_bar_color(is_dark)
        except Exception as e:
            pass

        #layout
        self.rowconfigure((0,1,2,3,4,5,6),weight=1,uniform='a')
        self.columnconfigure((0,1,2,3),weight=1,uniform='a')


        #data
        self.formula_str=ctk.StringVar()
        self.result_str=ctk.StringVar(value=0)
        self.output_list=[]
        self.formula_list=[]

        self.create_widgets()

        self.mainloop()

    def title_bar_color(self,is_dark):
        HWND  =windll.user32.GetParent(self.winfo_id())
        title_color  =TITLE_BAR_HEX['dark'] if is_dark else TITLE_BAR_HEX['light']
        windll.dwmapi.DwmSetWindowAttribute(HWND,35,byref(c_int(title_color)),sizeof(c_int))
        
    def create_widgets(self):
        font=ctk.CTkFont(family=FONT,size=NORMAL_FONT_SIZE)

        #calling
        output(self,0,'se',self.formula_str,font=ctk.CTkFont(family=FONT,size=NORMAL_FONT_SIZE))
        output(self,1,'e',self.result_str,font=ctk.CTkFont(family=FONT,size=OUTPUT_FONT_SIZE))
    
        #button
        Button(self,'AC',font,self.clr_btn)
        Button(self,'invert',font,self.inverrt_btn)
        Button(self,'perc',font,self.per_btn)
        
        #num_button

        for num in NUM_POSITION:
            num_buuton(self,num,font,self.num_keypress)

        #MATH_BUTTON
        for math in MATH_POSITIONS:
            math_pad(self,math,font,self.math_press)
        
        #calculations

    def num_keypress(self,num):

        if num =='.' and '.' in ''.join(self.output_list):
            return  self.num_keypress(0)

        else:
            self.output_list.append(str(num))
            self.result_str.set(value=''.join(self.output_list))
   
    def math_press(self,num):
        current_num=''.join(self.output_list)

        if current_num:
            self.formula_list.append(current_num)

            if num!='=':
                self.formula_list.append(num)
                self.output_list.clear()

                self.result_str.set('')
                self.formula_str.set(' '.join(self.formula_list))
                
            else:
                formula=' '.join(self.formula_list)
                result = eval(formula)

                #formating

                if isinstance(result,float):
                    if result.is_integer():
                        result = int(result)

                    else:
                        result = round(result,3)
                    
                self.formula_list.clear()
                self.output_list = [str(result)]

                self.result_str.set(result) 
                self.formula_str.set(formula)
        
    def clr_btn(self,):
        self.result_str.set(0)
        self.formula_str.set('')
        self.output_list.clear()
        self.formula_list.clear()

    def per_btn(self):
        current = ''.join(self.output_list)
        if current:
            current = float(''.join(self.output_list))
            percent=current/100

            self.output_list = list(str(percent))

            self.result_str.set(''.join(self.output_list))

    def inverrt_btn(self):
        current = ''.join(self.output_list)
        if current:
            if float(current)>0:
                self.output_list.insert(0,'-')

            else:
                del self.output_list[0]
        
            self.result_str.set(''.join(self.output_list))

class output(ctk.CTkLabel):
    def __init__(self,parent,row,anchor,strvar,font):
        super().__init__(parent,textvariable=strvar,font=font,)
        self.grid(row=row,column= 0,columnspan= 4,sticky= anchor)

class Button(ctk.CTkButton):
    def __init__(self, master,text,font,func):
        super().__init__(
            master,
            corner_radius=STYLING['corner-radius'], 
            fg_color = COLORS['dark-gray']['fg'],
            hover_color = COLORS['dark-gray']['hover'], 
            text_color =COLORS['dark-gray']['text'] , 
            text = OPERATORS[text]['text'], 
            font = font,
            command = lambda : func(), 
        )

        self.grid(row = OPERATORS[text]['row'],column=OPERATORS[text]['col'],padx=STYLING['gap'],pady= STYLING['gap'],sticky='nsew')

class num_buuton(ctk.CTkButton):
    def __init__(self, master, text, font,func):
        super().__init__(
            master,
            corner_radius=STYLING['corner-radius'], 
            fg_color = COLORS['light-gray']['fg'],
            hover_color = COLORS['light-gray']['hover'], 
            text_color =COLORS['light-gray']['text'] , 
            text = text, 
            font = font, 
            command = lambda : func(text), 
        )

        self.grid(row = NUM_POSITION[text]['row'],column=NUM_POSITION[text]['col'],columnspan=NUM_POSITION[text]['span'],padx=STYLING['gap'],pady= STYLING['gap'],sticky='nsew')

class math_pad(ctk.CTkButton):
        def __init__(self, master, text, font,func):
            super().__init__(
                master,
                corner_radius=STYLING['corner-radius'], 
                fg_color = COLORS['orange']['fg'],
                hover_color = COLORS['orange']['hover'], 
                text_color =COLORS['orange']['text'] , 
                text = MATH_POSITIONS[text]['character'], 
                font = font, 
                command = lambda : func(text), 
            )

            self.grid(row = MATH_POSITIONS[text]['row'],column=MATH_POSITIONS[text]['col'],padx=STYLING['gap'],pady= STYLING['gap'],sticky='nsew')



if __name__=='__main__':

    calc(darkdetect.isDark())