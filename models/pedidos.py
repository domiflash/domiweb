class Pedido:
    def __init__(self, idped, cliente, productos, total, estado="pendiente"):
        self.idped = idped
        self.cliente = cliente  # puede ser un dict {id, nombre, direccion}
        self.productos = productos  # lista de dicts {idpro, nombre, cantidad, precio}
        self.total = total
        self.estado = estado

    def to_dict(self):
        return {
            "idped": self.idped,
            "cliente": self.cliente,
            "productos": self.productos,
            "total": self.total,
            "estado": self.estado,
        }
