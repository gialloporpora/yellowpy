Questa è una piccola guida al markdown, il pseudo-linguaggio di formattazione creato da Aaron Schwartz e 

Lo scopo del markdown è quello di avere una sintassi semplice per la scrittura di file formattati.
Ovviamente col markdown non è possibile fare tutto quello che si può fare con HTML, quando serve è però possibile codice HTML nei file markdown e questo verrà interpretato come tale.


## Intestazioni

Sono possibili due diversi modi per le intestazioni:

Intestazione 1
==============

Intestazione 2
--------------

Per le altre intestazione di livello superiore è necessario utilizzare la sintassi con i cancelletti:


# Intestazione 1

## Intestazione 2

### Intestazione 3

#### Intestazione 4

##### Intestazione 5

###### Intestazione 6

Enfasi e grassetto

*Questo testo è enfatizzato*

**Questo testo è in grassetto**

***Questo testo è in super grassetto***

Una caratteristica del markdown di GitHub è quella di non riconoscere il simbolo \* come marcatore di formattazione se non è preceduto, o seguito, da un carattere bianco (spazi, tabulazioni).

Esempio io non p*oss*o evidenziare la parte di una *parola*.

Comporamento assai interessante è quello con la punteggiatura.

Tento di evidenziare una virgola*,* ciò non è possibile*.*

E così*?* O così *?*

Vediamo ora come si fanno gli elenchi puntati:

-   arance
-   mele
-   limoni

Oppure:

*   arance
*   mele
*   limoni

Si possono fare anche gli elenchi numerati:

1. arance
3.  limoni

Ma anche:

5.  arance
6.  mele
7.  limoni

Una regola non necessaria, ma utile, è la regola del quattro.
Usare sempre quattro caratteri per liste, citazioni e codice, questo aiuterà nell'indentazione di liste o citazioni con paragrafi o altri livelli di liste e citazioni.

1.  Questo è il primo elemento di una lista composta da paragrafi.
    Seguendo la regola del 4  è possibile rendere il sorgente ancora più leggibile.
2.  Questo è il secondo paragrafo della lista.
    Per i paragrafi successivi, gli editor avanzati, identeranno automecamente il testo aggiungendo gli spazi iniziali.
    Si può vedere come è scritto questo periodo nel sorgente per rendersene conto.
3.  Un aiuto ulteriore si ha se si includono altri elenchi puntati:
    
    1.  primo elemento della sottolista
    2.  secondo elemento della sottolista
    3.  terzo elemento della sottolista
    
    qui torniamo nell'elemento della lista principale.
4.  Ultimo elemento della lista principale.
    Anche esso un paragrafo.
    Se non si vogliono usare i quattro spazi si può usare un carattere di tabulazione, è la stessa cosa e molti editor hanno delle funzioni per passare dall'uno all'altro in modo rapido.
    
    
Sono supportati anche gli elenchi con puntatori alfabetici:

a.  Primo elemento di una lista con puntatori alfabetici.
b.  Secondo elemento di una lista con puntatori alfabetici.
c. Terzo elemento di una lista con puntatori alfabetici.


Per i puntatori con numeri romani bisognerà invece ritornare al codice HTML:

I.  I romani al posto di 1 scrivevano I.
II. Al posto del due scrivevano II.
III. AAl posto del tre III che  rompe la regola del quattro.
IV.  Il quattro è IV.
V.  Ma per questo tipo di elenchi serve HTML.



Con gli elenchi abbiamo finito.
Passiamo alle citazioni:

>   Questo è del testo quotato.
>   Il testo quotato rispetta lo standard usato nelle email di testo usando il carattere maggiore.

Quanto fatto sopra si può ottenere anche con la regola del quattro semplicemente indentando il seconla seconda riga:

>   Questo è il testo quotato.
    in un'altra maniera, il risultato è identico.
    E ricordati che finché non metti una riga completamente vuota, il testo continuerà a far parte della citazione (vedi sorgente).

    
    Per livelli di citazione multiple si usando più caratteri maggiori, come nelle email.
    
    >   Alice ha scritto:
    
>>  Bob ha scritto:
>>  Ciao Alice.
>>  Come stai?
>   Ciao Bob.
>   Io sto bene e tu


Torniamo a cose utili: testo preformattato, cioè reso con un carattere di tipo macchina da scrivere, in informatica questo è sinonimo di codice sorgente.

Per del codice inline si racchiude il testo tra backtick (accento grave \`), ad esempio `markdown`.


Per un blocco di codice si può usare la tabulazione del testo o marcare l'inizio e la fine del blocco di codice con tre backtick \`\`\`.


	def ciao(persona):
		print "Ciao %s" %persona

Ma anche:


```
	def ciao(persona):
	print "Ciao %s" %persona
```





## Link


[Questo è un link al sito di Mozilla](Https://www.mozilla.org)

[Questo è un link al sito di Mozilla](https://www.mozilla.org)



[Link javascript](javascript:alert(123);)



## Immagini



![Favicon sito Mozilla](https://www.mozilla.com/media/img/firefox/favicon-196.223e1bcaf067.png)

Si possono anche linkare le immagini:

[![Favicon sito Mozilla](https://www.mozilla.com/media/img/firefox/favicon-196.223e1bcaf067.png)](https://www.mozilla.com)


È anche possibile uno stile alternativo per i link che rende ancora più leggibile il sorgente e cioé facendo riferimento ad essi come se fossero delle note.
Per farlo, a fine documento, bisogna tenere traccia di questi riferimenti, ad esempio:

	[link1]: https://www.mozilla.com


A questo punto sarà possibile riferirsi al link inserendolo fra parentesi quadre e non fra parentesi tonde come i veri link.

	[Link al sito Mozilla][link1]

[Link al sito Mozilla][link1]

Il markdown su Github ha la particolarità di non considerare le righe come dei nuovi paragrafi.
Per iniziare un nuovo paragrafo è necessario inserire una riga bianca.
Per andare a capo all'interno di un paragrafo o tra i paragrafi basta mettere uno spazio finale alla riga precedente oppure usare il carattere `\\`. 
Questo interromperà il paragrafo con un `<br/>`, però no mpm  creerà un nuovo paragrafo come quando si incontra una riga bianca.

Nuovo paragrafo.
Riga due. 
Interrotta.
Questa è una nuova riga.\\
Interotta nuovamente.


## Numeri e simboli matematici

Il markdown di pandoc riconosce anche il codice LaTeX quando inserito nei blocchi separati da `$$`.
Non credo che su GitHub funzioni. 
giusto una prova:


$$
x^2 + y^2 = 1
$$


Probabilmente non funziona, però, potrebbe funzionare:

x^2^ + y^2^ = 1

o anche:

x_0_^2^ + x_1_^2^ = 1








[link1]: https://www.mozilla.com