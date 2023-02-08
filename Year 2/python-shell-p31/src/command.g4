grammar command;

/*
 * Lexer Rules
 */

WHITE_SPACE: (' ' | '\t');
SINGLE_QUOTES: '\'' (~['\n])+ '\'';
BACK_QUOTES: '`' (~[`\n])+ '`';
DOUBLE_QUOTES: '"' (BACK_QUOTES | (~[`"\n])+)* '"';
TEXT: (~[ '"`|<>;\t\n])+;

/*
 * Parser Rules
 */

command: ((call pipe?) sequence?)? EOF ;
pipe: '|' call pipe?;
sequence: ';' (call pipe?) sequence? ;
call: WHITE_SPACE* (redirection WHITE_SPACE*)* argument (WHITE_SPACE* atom)* WHITE_SPACE*;

atom: redirection | argument;
argument: ( quoted | TEXT )+;
redirection: ('<' WHITE_SPACE* argument) | '>' WHITE_SPACE* argument;
quoted: SINGLE_QUOTES | DOUBLE_QUOTES | BACK_QUOTES;
