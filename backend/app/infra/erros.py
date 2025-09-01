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

class NotFoundError(Exception):
    def __init__(self, message=None, cause=None, action=None):
        self.message = message or "Não foi possível encontrar este recurso no sistema."
        self.cause = cause
        self.name = self.__class__.__name__
        self.action = action or  "Verifique se os parâmetros enviados na consulta estão certos."
        self.status_code = 404
        super().__init__(self.message)

    def to_dict(self):
        return {
            "name": self.name,
            "message": self.message,
            "action": self.action,
            "status_code": self.status_code,
        }

class InternalServerError(Exception):
        def __init__(self, cause=None, status_code=500):
            super().__init__("Um erro interno não esperado aconteceu.")
            self.name = self.__class__.__name__
            self.cause = cause
            self.action = "Entre em contato com o suporte."
            self.status_code = status_code

        def to_dict(self):
            return {
                "name": self.name,
                "message": str(self),
                "action": self.action,
                "status_code": self.status_code,
                "cause": str(self.cause) if self.cause else None,
            }