class ValidationError(Exception):
    def __init__(self, message=None, cause=None, action=None):
        self.message = message or "Um erro de validação ocorreu"
        self.cause = cause
        self.name = self.__class__.__name__
        self.action = action or "Verifique os dados enviados e tente novamente."
        self.status_code = 400
        super().__init__(self.message)

    def to_dict(self):
        return {
            "name": self.name,
            "message": self.message,
            "action": self.action,
            "status_code": self.status_code,
        }