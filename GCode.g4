grammar GCode;

// =============================================
// REGRAS DO PARSER (minúscula)
// =============================================

program      : declaration* programEnd;

programEnd   : M30;

declaration  : variable | statement | function;

statement    : lineNumber codFunc detail* LINE_END;

// o comando de interpolação circular não necessariamente recebe o raio
detail       : coord | delta_center | stop_ms; 

lineNumber   : N INT;

codFunc      : GCODE;

coord        : DIR MINUS? (FLOAT | INT); 

delta_center : DELTA MINUS? (FLOAT | INT); // clockwise - removidos parênteses desnecessários

stop_ms      : P INT;

variable     : VAR ID ASSIGN MINUS? (FLOAT | INT) LINE_END; // Adicionado LINE_END

function     : FUNC ID LPAREN parameterList? RPAREN LBRACE declaration* RBRACE;

parameterList: parameter (COMMA parameter)*;

parameter    : ID (ASSIGN MINUS? (FLOAT | INT))?;

// =============================================
// REGRAS DO LEXER (MAIÚSCULA)
// =============================================

// Códigos G de funções a serem utilizadas
GCODE   : 'G00' | 'G01' | 'G02' | 'G03' | 'G04';

// Comandos M
M30     : 'M30'; // acaba o programa

// Coordenadas e parâmetros
DIR     : 'X' | 'Y';
DELTA   : 'I' | 'J';
P       : 'P'; // ms de parada
N       : 'N'; // Número de Linha 
T       : 'T'; // graus de interpolação circular

// Palavras-chave
VAR     : 'VAR';
FUNC    : 'FUNC';

// Literais
FLOAT   : [0-9]+ '.' [0-9]+;  // Movido antes de INT para prioridade
INT     : [0-9]+;

// Identificadores (movido após literais para evitar conflitos)
ID      : [a-zA-Z][a-zA-Z0-9]*;

// Operadores e delimitadores
MINUS   : '-';
ASSIGN  : '=';
LBRACE  : '{';
RBRACE  : '}';
LPAREN  : '(';
RPAREN  : ')';
COMMA   : ',';

// Terminadores e whitespace
LINE_END: '\r'? '\n'; 
WS      : [ \t\r\n]+ -> skip;