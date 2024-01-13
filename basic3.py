#######################################
# CONSTANTS
#######################################

BILANG = '0123456789'
TITIK_MALAKI = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
TITIK_MALIIT = 'abcdefghijklmnopqrstuvwxyz'
ALPABETO = TITIK_MALAKI + TITIK_MALIIT
ISPESYAL_NA_SIMBOLO = ',, (, ), {, }, “, /, _, -, @, !, %, &, <, >, +, =, ^, |, \, ;, :, ., <patlang>'
SIMBOLO = BILANG + ALPABETO  

#######################################
# ERRORS
#######################################

class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details
    
    def as_string(self):
        result  = f'{self.error_name}: {self.details}\n'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        return result

class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)

#######################################
# POSITION
#######################################

class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

#######################################
# TOKENS
#######################################

TT_INT		= 'INT'
TT_FLOAT    = 'FLOAT'
TT_PLUS     = 'PLUS'
TT_MINUS    = 'MINUS'
TT_MUL      = 'MUL'
TT_DIV      = 'DIV'
TT_LPAREN   = 'LPAREN'
TT_RPAREN   = 'RPAREN'
TT_IDEN     = 'IDENTIFIER'
TT_STRING   = 'STRING'

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value
    
    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'

#######################################
# LEXER
#######################################

class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()
    
    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in BILANG:
                tokens.append(self.make_number())
            elif self.current_char in ALPABETO + '_':
                if self.current_char == 'a' or 'A':
                    tokens.append(self.a_key())
                elif self.current_char == 'b' or 'B':
                    tokens.append(self.b_key())
                elif self.current_char == 'c' or 'C':
                    tokens.append(self.c_key())
                elif self.current_char == 'd' or 'D':
                    tokens.append(self.d_key())
                elif self.current_char == 'e' or 'E':
                    tokens.append(self.e_key())
                elif self.current_char == 'f' or 'F':
                    tokens.append(self.f_key())
                elif self.current_char == 'g' or 'G':
                    tokens.append(self.g_key())
                elif self.current_char == 'h' or 'H':
                    tokens.append(self.h_key())
                elif self.current_char == 'i' or 'I':
                    tokens.append(self.i_key())
                elif self.current_char == 'j' or 'J':
                    tokens.append(self.j_key())
                elif self.current_char == 'k' or 'K':
                    tokens.append(self.k_key())
                elif self.current_char == 'l' or 'L':
                    tokens.append(self.l_key())
                elif self.current_char == 'm' or 'M':
                    tokens.append(self.m_key())
                elif self.current_char == 'n' or 'N':
                    tokens.append(self.n_key())
                elif self.current_char == 'ñ' or 'Ñ':
                    tokens.append(self.ñ_key())
                elif self.current_char == 'o' or 'O':
                    tokens.append(self.o_key())
                elif self.current_char == 'p' or 'P':
                    tokens.append(self.p_key())
                elif self.current_char == 'q' or 'Q':
                    tokens.append(self.q_key())
                elif self.current_char == 'r' or 'R':
                    tokens.append(self.r_key())
                elif self.current_char == 's' or 'S':
                    tokens.append(self.s_key())
                elif self.current_char == 't' or 'T':
                    tokens.append(self.t_key())
                elif self.current_char == 'u' or 'U':
                    tokens.append(self.u_key())
                elif self.current_char == 'v' or 'V':
                    tokens.append(self.v_key())
                elif self.current_char == 'w' or 'W':
                    tokens.append(self.w_key())
                elif self.current_char == 'x' or 'X':
                    tokens.append(self.x_key())
                elif self.current_char == 'y' or 'Y':
                    tokens.append(self.y_key())
                elif self.current_char == 'z' or 'Z':
                    tokens.append(self.z_key())
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN))
                self.advance()
            
            elif self.current_char == "\"":
                tokens.append(self.make_str())
                self.advance()

            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0

        while self.current_char != None and self.current_char in BILANG + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TT_INT, int(num_str))
        else:
            return Token(TT_FLOAT, float(num_str))
    

    def make_str(self):
        char_str = ''

        if self.current_char == "\"":
            self.advance()
            while self.current_char != "\"":
                char_str += self.current_char
                self.advance()
            return Token(TT_STRING, char_str)
        

    ####def make_letter(self):
       # let_str = ''

    #    while self.current_char != None and self.current_char in TITIK_MALIIT or TITIK_MALAKI:
    #        let_str += self.current_char
    #        self.advance()
     #   return Token(TT_CHAR, str(let_str))
    
    ####
        
    def a_key(self):
        key_str = self.current_char
        self.advance()
        return self.identifier(key_str)
    
    def b_key(self):
        key_str = self.current_char
        self.advance()
        return self.identifier(key_str)
    def c_key(self):
        key_str = self.current_char
        self.advance()
        return self.identifier(key_str)

    def d_key(self):
        key_str = self.current_char
        self.advance()
        return self.identifier(key_str)
    
    def e_key(self):
        key_str = self.current_char
        self.advance()
        return self.identifier(key_str)

    def f_key(self):
        key_str = self.current_char
        self.advance()
        return self.identifier(key_str)

    def g_key(self):
        key_str = self.current_char
        self.advance()
        return self.identifier(key_str)

    def h_key(self):
        key_str = self.current_char
        self.advance()
        return self.identifier(key_str)

    def i_key(self):
        key_str = self.current_char
        self.advance()
        return self.identifier(key_str)

    def j_key(self):
        key_str = self.current_char
        self.advance()
        return self.identifier(key_str)

    def k_key(self):
        key_str = self.current_char
        self.advance()
        return self.identifier(key_str)

    def l_key(self):
        key_str = self.current_char
        self.advance()
        return self.identifier(key_str)

    def m_key(self):
        key_str = self.current_char
        self.advance()
        return self.identifier(key_str)

    def n_key(self):
        key_str = self.current_char
        self.advance()
        return self.identifier(key_str)

    def ñ_key(self):
        key_str = self.current_char
        self.advance()
        return self.identifier(key_str)

    def o_key(self):
        key_str = self.current_char
        self.advance()
        return self.identifier(key_str)

    def p_key(self):
        key_str = self.current_char
        self.advance()
        return self.identifier(key_str)

    def q_key(self):
        key_str = self.current_char
        self.advance()
        return self.identifier(key_str)

    def r_key(self):
        key_str = self.current_char
        self.advance()
        return self.identifier(key_str)

    def s_key(self):
        key_str = self.current_char
        self.advance()
        return self.identifier(key_str)

    def t_key(self):
        key_str = self.current_char
        self.advance()
        return self.identifier(key_str)

    def u_key(self):
        key_str = self.current_char
        self.advance()
        return self.identifier(key_str)

    def v_key(self):
        key_str = self.current_char
        self.advance()
        return self.identifier(key_str)

    def w_key(self):
        key_str = self.current_char
        self.advance()
        return self.identifier(key_str)

    def x_key(self):
        key_str = self.current_char
        self.advance()
        return self.identifier(key_str)

    def y_key(self):
        key_str = self.current_char
        self.advance()
        return self.identifier(key_str)

    def z_key(self):
        key_str = self.current_char
        self.advance()
        return self.identifier(key_str)

    def identifier(self, key_str):
     id_str = key_str

     while self.current_char != None and self.current_char in SIMBOLO + '_':
        id_str += self.current_char
        self.advance()
    
     return Token(TT_IDEN, id_str)
    
  # |> KEYWORDS, RESERVED WORDS, NOISE WORDS, BOOLEANS <| #

#######################################
# RUN
#######################################

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()

    return tokens, error