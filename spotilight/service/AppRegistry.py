class AppRegistry:
    
    session_state = None
    
    @classmethod
    def set_session_state(cls, session_state):
        cls.session_state = session_state
        
    @classmethod    
    def get_session_state(cls):
        return cls.session_state