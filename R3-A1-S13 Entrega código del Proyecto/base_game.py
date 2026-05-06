class BaseGame:
    def __init__(self, id_sesion, nombre_juego):
        self.id_sesion = id_sesion
        self.nombre_juego = nombre_juego
        self.resultado_temporal = {
            "id_sesion": id_sesion,
            "puntaje": 0,
            "aciertos": 0,
            "errores": 0,
        }

    def guardar_backup_local(self):
        print(f"Action triggered: backup.local:{self.nombre_juego}")

    def enviar_backup_si_existe(self):
        print(f"Action triggered: backup.sync:{self.nombre_juego}")

    def guardar_resultado_final(self):
        print(f"Action triggered: result.final:{self.nombre_juego}")

    def actualizar_resultados(self, puntaje=None, aciertos=None, errores=None):
        if puntaje is not None:
            self.resultado_temporal["puntaje"] = puntaje
        if aciertos is not None:
            self.resultado_temporal["aciertos"] = aciertos
        if errores is not None:
            self.resultado_temporal["errores"] = errores