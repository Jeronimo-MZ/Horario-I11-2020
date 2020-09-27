import sqlite3, datetime, pyperclip
import sys, os
class DataBase:
	def __init__(self, nome="Horario.db", ):
		self.__table_name = "Horario"
		self.__database_name = nome
		abs_path = os.path.abspath(sys.argv[0]+"/..")
        # usando caminho absoluto para poder usar atalhos para executar
		# print(abs_path)
		self.conn = sqlite3.connect(abs_path + "/" + self.__database_name)
		self.cursor = self.conn.cursor()
		self.CreateTable()

	def CreateTable(self):
		self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.__table_name}(DiaSemana TEXT, NomeDisciplina TEXT, \
			Inicio Integer, Fim Integer, IdSala Text)")
		self.save()

	def adicionarAula(self, DiaSemana, NomeDisciplina, Inicio, Fim, IdSala):
		self.cursor.execute(f'INSERT INTO {self.__table_name} \
			VALUES("{DiaSemana}", "{NomeDisciplina}", {Inicio}, {Fim}, "{IdSala}")')
		self.save()

	def procurarAula(self, DiaSemana, horaActual):
		self.cursor.execute(f'SELECT * FROM {self.__table_name} WHERE DiaSemana="{DiaSemana}"');
		aulas = self.cursor.fetchall()
		if aulas is not None:
			for aula in aulas:
				if self.match(aula, horaActual):
					return (aula[1], aula[-1])
		return None

	def match(self, aula, horaActual):
		if horaActual >= int(aula[2])  and horaActual < int(aula[3]) :
			return True
		return False

	def save(self):
		self.conn.commit()

	def close(self):
		self.conn.close()

## 972-886-3709
### DateTime
def obterDataActual():
	data = datetime.datetime.now()
	diaSemana = data.strftime("%A")
	horaActual = str(data).split()[1]
	horaActual = int(horaActual.split(":")[0])
	## return ("Monday", 11)
	return (diaSemana, horaActual)

if __name__ == '__main__':
	instance = DataBase()
	data = obterDataActual()
	aula = instance.procurarAula(data[0], data[1])
	if aula is not None:
		print(f"Disciplina: {aula[0]}\nID: {aula[1]}")
		pyperclip.copy(str(aula[1]))
		print("ID copiado para área de Tranferência!")
	else:
		print("Não há nenhuma Aula para esta data")
	input("Clique 'ENTER' para sair")
	# Its Working ^-^
	instance.close()
