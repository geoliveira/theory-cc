import re

'''
I) Analise o código disponível em Linguagem L em busca de possíveis falhas e destaque os seus pontos positivos e negativos
R: O código está funcional e faz com que seja possível entender a expectativa do Professor em relação ao intepretador da linguagem L. A linguagem utilizada para construir o interpretador da linguagem L pode tornar o desenvolvimento do interpretador mais prático e rápido se o desenvolvedor já tiver familiaridade com a linguagem utilizada. Caso não tenha familiaridade com a linguagem utilizada, particularmente, acredito que alguns comentários de documentação em certos pontos e tornar explícito os tipos das variáveis/argumentos/saídas poderiam ajudar no entendimento do código.

II) Corrija essas eventuais falhas, deixe o código mais robusto e implemente algumas funcionalidades que deixem esse interpretador mais útil e prático (sem mudar a linguagem que será executada).
R: 
'''

KEYWORDS = {'IF', 'GOTO'} # all keywords
RE_LABEL_NAME = r"^(A|B|C|D|E|[A|B|C|D|E][1-9][0-9]*)$" # all label's name
RE_LABEL = r"^\[.\]$" # label's check
RE_VARIABLE = r"^(X|Z|Y|[X|Z][1-9][0-9]*)$" # input, local, and output variables
RE_IL_VARIABLE = r"^(X|Z|[X|Z][1-9][0-9]*)$" # input and local variables only
RE_OPERATOR = r"[+\-*/]" # arithmetic operators
RE_CUSTOM_OPERATOR = r"(\<\>)|(\<\-)" # custom operators
RE_ID = r"[A-Za-z]+" # identifiers
RE_NUMBER = r"\d+" # integer

token_specification = {
	'label': RE_LABEL,
	'variable': RE_IL_VARIABLE,
	'custom_operator': RE_OPERATOR,
	'operator': RE_CUSTOM_OPERATOR,
	'id': RE_ID,
	'number': RE_NUMBER,
}

pattern = '|'.join('(?P<%s>%s)' % pair for pair in token_specification.items())

def set_input_variable(variable: str) -> int:
	return 1
	return int(
		input(
			"Digite o valor de entrada da variável " + variable + ": "
		)
	)

class Interpreter:
	def __init__(self):
		self.variables: dict[str, int] = {"Y": 0}
		self.labels: dict[str, int] = {}
		self.current_line: int = 0

	def interpret(self, program):
		lines = program.split("\n")
		self.compile_labels_vars(lines)
		size = len(lines)
		while self.current_line < size:
			line = lines[self.current_line].strip()
			self.execute_instruction(line)
			if self.current_line == -1:
				self.current_line = size

	def compile_labels_vars(self, lines):
		regex = re.compile(pattern)
		for idx, line in enumerate(lines):
			tokens = line.split()
			for token in tokens:
				mo = regex.fullmatch(token)
				group = mo.lastgroup
				match group:
					case 'label':
						label = token[1:-1] # adiciona somente o nome, i.e sem os colchetes
						if label not in self.labels:
							self.labels[label] = idx
					case 'variable':
						if token not in self.variables:
							self.variables[token] = 0 if token[0] == "Z" else set_input_variable(token)
					case _:
						if group in token_specification.keys():
							continue
						raise RuntimeError(f"Token está fora do padrão: '{token}'")

	def execute_instruction(self, line):
		regex = re.compile(pattern)
		tokens = line.split()
		if not tokens:
			self.current_line += 1
			return
		mo = regex.fullmatch(tokens[0])
		if mo.lastgroup == 'label':
			tokens.pop(0)
		# IF V <> 0 GOTO L
		#  If the value of V is nonzero, perform the instruction with label L next;
		#   otherwise proceed to the next instruction in the list.
		if (
			tokens[0] == "IF"
			and tokens[2:5] == ["<>", "0", "GOTO"]
			and len(tokens) == 6
		):
			variable = tokens[1]
			label = tokens[5]
			value = self.get_variable_value(variable)
			if value != 0:
				if tokens[5] in self.labels:
					self.current_line = self.labels[label]
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
			# V <- V + 1
			#  Increase by I the value of the variable V. 
			if operator == "+":
				self.set_variable(variable, self.get_variable_value(variable) + 1)
			# V <- V - 1
			#  If the value of V is 0, leave it unchanged;
			#   otherwise decrease by I the value of V
			elif operator == "-":
				self.set_variable(variable, self.get_variable_value(variable) - 1)
			else:
				print("Erro de sintaxe na linha " + self.current_line)
			self.current_line += 1
		else: print("Erro de sintaxe na linha " + self.current_line)

	def get_variable_value(self, variable: str) -> int:
		return self.variables[variable] if variable in self.variables else 0

	def set_variable(self, variable: str, value: int):
		self.variables[variable] = value if value > 0 else 0


'''
Referências

<>		: operador diferença, referente ao '!=' em python
<-		: operação de atribuição, referente ao '=' em python
GOTO	: comando que pula para label indicada, referente ao 'goto' do C/C++
'''
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
