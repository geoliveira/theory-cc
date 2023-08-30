import re


class Interpreter:
	def __init__(self):
		self.variables = {"Y": 0}
		self.labels = {}
		self.current_line = 0

	def interpret(self, program):
		lines = program.split("\n")
		self.compile_labels_vars(lines)
		size = len(lines)
		while self.current_line < size:
			line = lines[self.current_line].strip()
			self.execute_instruction(line)
			if self.current_line == -1:
				self.current_line = size

	def compile_var(self, variable):
		varregex = re.search(r"^(X|Y|Z|[X|Z][1-9][0-9]*)$", variable)
		if varregex:
			if variable[0] == "Z":
				if variable not in self.variables:
					self.variables[variable] = 0
			elif variable[0] == "X":
				if variable not in self.variables:
					self.variables[variable] = int(
						input(
							"Digite o valor de entrada da variável " + variable + ": "
						)
					)
		else:
			print("Variável " + variable + " fora do padrão!")

	def compile_labels_vars(self, lines):
		for i, line in enumerate(lines):
			tokens = line.split()
			if tokens and tokens[0].startswith("[") and tokens[0].endswith("]"):
				label = tokens[0][1:-1]
				labelregex = re.search(r"^(A|B|C|D|E|[A|B|C|D|E][1-9][0-9]*)$", label)
				if labelregex:
					if label not in self.labels:
						self.labels[label] = i
				else:
					print("Label " + label + " fora do padrão!")
				if tokens[1] == "IF":
					self.compile_var(tokens[2])
				else:
					self.compile_var(tokens[1])
			elif tokens:
				if tokens[0] == "IF":
					self.compile_var(tokens[1])
				else:
					self.compile_var(tokens[0])

	def execute_instruction(self, line):
		tokens = line.split()
		if not tokens:
			self.current_line += 1
			return
		if tokens and tokens[0].startswith("[") and tokens[0].endswith("]"):
			tokens.pop(0)
		if (
			tokens[0] == "IF"
			and tokens[2:5] == ["<>", "0", "GOTO"]
			and len(tokens) == 6
		):
			labelregex = re.search(r"^(A|B|C|D|E|[A|B|C|D|E][1-9][0-9]*)$", tokens[5])
			if not labelregex:
				print("Label " + tokens[5] + " fora do padrão!")
			variable = tokens[1]
			value = self.get_variable_value(variable)
			if value != 0:
				if tokens[5] in self.labels:
					self.current_line = self.labels[tokens[5]]
				else:
					self.current_line = -1
			else:
				self.current_line += 1
		elif (
			tokens[0] == tokens[2]
			and tokens[1] == "<-"
			and tokens[4] == "1"
			and len(tokens) == 5
		):
			variable = tokens[0]
			operator = tokens[3]
			if operator == "+":
				current_value = self.get_variable_value(variable)
				self.set_variable(variable, current_value + 1)
			elif operator == "-":
				current_value = self.get_variable_value(variable)
				if current_value > 0:
					self.set_variable(variable, current_value - 1)
			else:
				print("Erro de sintaxe na linha " + self.current_line)
			self.current_line += 1

	def get_variable_value(self, variable):
		if variable in self.variables:
			return self.variables[variable]
		return 0

	def set_variable(self, variable, value):
		self.variables[variable] = value


# Exemplo de programa (programa (c) da página 20 com a macro GOTO expandida)
program = """
[A] IF X <> 0 GOTO B
	Z2 <- Z2 + 1
	IF Z2 <> 0 GOTO C
[B] X <- X - 1
	Y <- Y + 1
	Z <- Z + 1
	Z2 <- Z2 + 1
	IF Z2 <> 0 GOTO A
[C] IF Z <> 0 GOTO D
	Z2 <- Z2 + 1
	IF Z2 <> 0 GOTO E
[D] Z <- Z - 1
	X <- X + 1
	Z2 <- Z2 + 1
	IF Z2 <> 0 GOTO C
"""
print(program)  # Imprime o programa a ser executado

interpreter = Interpreter()
interpreter.interpret(program)
print(interpreter.variables)  # Imprime os valores das variáveis após a execução do programa
