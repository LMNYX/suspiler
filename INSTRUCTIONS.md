# Possible instructions

| Instruction | Description |
|---|---|
| START | GAME or MEETING (Script should start with START GAME) |
| END | GAME or MEETING (Script should end with END GAME) |
| SAY | Says everything after operation if meeting is called, can use *(VARIABLE) to say it's value |
| REMEMBER (VARIABLE) SUS/CREW | Sets variable to true/false |
| (VARIABLE) IS (...) | Sets a variable to any data (not true/false) |
| KILL (VARIABLE) | Removes the variable |
| VOTE (VARIABLE) | Adds 1 to the variable |
| DEFINE (...) (...) | Only available is DEFINE TASK (...), defines a loop |
| DO (...) (ONCE) | Only available is DO TASK (...), add ONCE at the end to not loop. |