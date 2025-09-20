class Producto:
	def __init__(self, idpro=None, idres=None, idcat=None, nompro=None, despro=None, prepro=None, imgpro=None, stopro=None):
		self.idpro = idpro
		self.idres = idres
		self.idcat = idcat
		self.nompro = nompro
		self.despro = despro
		self.prepro = prepro
		self.imgpro = imgpro
		self.stopro = stopro

	def to_dict(self):
		return {
			'idpro': self.idpro,
			'idres': self.idres,
			'idcat': self.idcat,
			'nompro': self.nompro,
			'despro': self.despro,
			'prepro': self.prepro,
			'imgpro': self.imgpro,
			'stopro': self.stopro
		}

	# Métodos CRUD pueden agregarse aquí según el ORM o conexión que uses
