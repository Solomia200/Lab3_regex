from __future__ import annotations
from abc import ABC, abstractmethod


class State(ABC):
    
    @abstractmethod
    def __init__(self) -> None:
        self.next_states: list[State] = []

    @abstractmethod
    def check_self(self, char: str) -> bool:
        """
        function checks whether occured character is handled by current ctate
        """
        pass

    def check_next(self, next_char: str) -> State | Exception:
        for state in self.next_states:
            if state.check_self(next_char):
                return state
            if isinstance(state, StarState) and (not state.check_self(next_char)):
                return state.check_next(next_char)

           

                
        raise NotImplementedError("rejected string")


class StartState(State):
  
    def __init__(self):
        super().__init__()
        


    def check_self(self, char):
        return True
    def __str__(self) -> str:
        return "StartState"

class TerminationState(State):
    
    
    def __init__(self):
        super().__init__()
    
    def check_self(self, char):
       
        return False
    
    def __str__(self) -> str:
        return "TerminationState"

class DotState(State):
    """
    state for . character (any character accepted)
    """

    

    def __init__(self):
        super().__init__()
        

    def check_self(self, char: str):
        
        return True
    
    def __str__(self) -> str:
        return "DotState"


class AsciiState(State):
    """
    state for alphabet letters or numbers
    """

   
    # curr_sym = ""

    def __init__(self, symbol: str) -> None:
        self.symbol = symbol
        self.next_states: list[State] = []


    def check_self(self, curr_char: str) -> State | Exception:
       
        return self.symbol == curr_char
    
    
    def __str__(self) -> str:
        return f"AsciiState({self.symbol} str)"


class StarState(State):

   

    def __init__(self, checking_state: State):
        self.next_states: list[State] = []
        self.checking_state = checking_state
        self.next_states.append(self)

    def check_self(self, char):
        
        return self.checking_state.check_self(char)
       
    def check_next(self, next_char: str) -> State | Exception:
       
        for state in self.next_states[1:]:
            if state.check_self(next_char):
                return state
            if isinstance(state, StarState) and (not state.check_self(next_char)):
                return state.check_next(next_char)
        
        
        if self.check_self(next_char):
            return self 
        raise NotImplementedError("rejected string")
            
          
    def __str__(self) -> str:
        return f"StarState({self.checking_state})"

class PlusState(State):
    

    def __init__(self, checking_state: State):
        self.checking_state = checking_state
        self.next_states: list[State] = []
        self.next_states.append(self)


    def check_self(self, char):
        
        return self.checking_state.check_self(char)
    def check_next(self, next_char: str) -> State | Exception:
         
        for state in self.next_states[::-1]:
            if state.check_self(next_char) :
              
                return state
            if isinstance(state, StarState) and (not state.check_self(next_char)) and (not self.check_self(next_char) ) :
                return state.check_next(next_char)
        if self.check_self(next_char):
            return self
        raise NotImplementedError("rejected string") 
    def __str__(self) -> str:
        return f"PlusState({self.checking_state})"

class RegexFSM:
    curr_state: State = StartState()

    def __init__(self, regex_expr: str) -> None:

        prev_state = self.curr_state
        tmp_next_state = self.curr_state

        for char in regex_expr:
            next_state= self.__init_next_state(char, prev_state, tmp_next_state)
            tmp_next_state.next_states.append( next_state)
           
            prev_state = tmp_next_state
            tmp_next_state = next_state  

           
            

        termination_state = TerminationState()
        tmp_next_state.next_states.append(termination_state)
    def __init_next_state(
        self, next_token: str, prev_state: State, tmp_next_state: State
    ) -> State:
        new_state = None

        match next_token:
            case next_token if next_token == ".":
                new_state = DotState()

            case next_token if next_token == "*":
                new_state =prev_state.next_states.pop()
                 
                
                new_state = StarState(  new_state)
                prev_state.next_states.append(new_state)

               

            case next_token if next_token == "+":
                new_state =prev_state.next_states.pop()
                new_state= PlusState( tmp_next_state)
                prev_state.next_states.append(new_state) 
                
            case next_token if next_token.isascii():
                
                new_state = AsciiState(next_token)

            case _:
                raise AttributeError("Character is not supported")

        return new_state
   
    def check_string(self,characters):
        current_state = self.curr_state
        for char in characters:
            try:
               
                current_state = current_state.check_next(char)
                
            except NotImplementedError:
                return False
       
        return any(isinstance(state, TerminationState) for state in current_state.next_states)

    def print_automaton(self):
        visited = set()
        stack = [self.curr_state]

       
        while stack:
            state = stack.pop()
            if state in visited:
                continue
            visited.add(state)
            print(f"{state} -> {[str(next_state) for next_state in state.next_states]}")
            stack.extend(state.next_states)


if __name__ == "__main__":
    regex_pattern = "a*4+g*hi"

    regex_compiled = RegexFSM(regex_pattern)
    # regex_compiled.print_automaton()
    print(regex_compiled.check_string("aaaaaa444ghi"))  # True
    print(regex_compiled.check_string("4hi"))  # True
    print(regex_compiled.check_string("meow"))  # False

    regex_pattern = "a*4+g*hi"
    regex_compiled = RegexFSM(regex_pattern)
    # regex_compiled.print_automaton()
    print(regex_compiled.check_string("aaaaaa444ghi"))  # True
    print(regex_compiled.check_string("4hi"))  # True
    print(regex_compiled.check_string("meow"))  # False
