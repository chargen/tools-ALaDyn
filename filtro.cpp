# include <leggi_binario_ALaDyn_fortran.h>
# include <stdarg.h>
/*
                                   _Filtro

è una struct orientata al filtraggio dei dati provenienti da simulazioni ALaDyn

Al momento sono contemplati filtri di soglia minima e massima per

                       CIASCUNA COORDINATA DI SPAZIO DI FASE
e per
                                 ENERGIA

Quest'ultima è, al presente, valutata da _Filtro stessa, ma si può molto
facilmente introdurre modifiche per evitarne il calcolo, così come introdurre
altri filtraggi su altre variabili e secondo altri criteri (Ad Majora).

Questo file fornisce anche nomi mnemonici #define-iti per le costanti intere
con un solo bit acceso -- INDIPENDENTEMENTE QUINDI DA MSB o LSB ----

                           STRUTTURA DEL CODICE

Il
                              namespace cost

definisce al suo interno nomi mnemonici per i filtri da applicare: ad esempio

                               cost :: xmin

serve ad attivare il filtro di soglia minima per la coordinata di fase X e

                               cost :: ymin | cost :: pzmax

attiva SIMULTANEAMENTE i filtri di soglia minima e massima per le coordinate di
fase X e Pz. Ciò viene fatto utilizzando alcune (non tutte) delle citate costanti
#define-ite.

                               cost :: tutte

raggruppa in un array ordinato tutte le precedenti costanti ed è utile per poter
gestire i loop.

                              DESCRIZIONE DELLA struct _Filtro

La enum class _Nomi serve a "battezzare" con nomi mnemonici di valori
CONSECUTIVI le stesse costanti del namespace cost; lo stesso fa l'array static
_Filtro :: cost ma usando degli unsigned int.

I metodi static

                         double * _Filtro :: costruisci_filtro
                             void _Filtro :: individua_filtro

lavorando in coppia, risparmiano al programmatore la grana di doversi ricordare
checchessia (nomi dei filtri, ordine di presenza negli array e quant'altro).

La variabile static maschera_interna e la struct flag_filtri sono trasparenti
all'utente finale.

L'array di stringhe _Filtro :: descr è utile per trasmettere i richiesti
argomenti alla funzione _Filtro :: costruisci_filtro.

Il costruttore di _Filtro fa tutto il lavoro: può essere eseguito fornendogli
quattro parametri oppure solo tre, lasciandogli l'arbitrio del quarto (ma solo
se viene usato come terzo parametro il valore reso da costruisci_filtro).

Il primo argomento da fornire al costruttore è, ovviamente, il puntatore ai
dati da filtrare; il secondo è un puntatore a due interi che siano,
nell'ordine, il numero di "particelle" e il numero di dati per particella.
Il terzo argomento è un array ordinato di valori double che contiene le diverse
soglie da utilizzare per la filtratura. Il quarto, se fornito, rappresenta i
filtri da applicare; se non fornito viene costruito da "costruisci_filtro"
assieme all'array da usare come terzo argomento.

Il main (commentato) che conclude il file esemplifica un paio di esecuzioni
tipiche.

*/
# define __0X00 0x1
# define __0X01 0x2
# define __0X02 0x4
# define __0X03 0x8
# define __0X04 0x10
# define __0X05 0x20
# define __0X06 0x40
# define __0X07 0x80
# define __0X08 0x100
# define __0X09 0x200
# define __0X10 0x400
# define __0X11 0x800
# define __0X12 0x1000
# define __0X13 0x2000
# define __0X14 0x4000
# define __0X15 0x8000
# define __0X16 0x10000
# define __0X17 0x20000
# define __0X18 0x40000
# define __0X19 0x80000
# define __0X20 0x100000
# define __0X21 0x200000
# define __0X22 0x400000
# define __0X23 0x800000
# define __0X24 0x1000000
# define __0X25 0x2000000
# define __0X26 0x4000000
# define __0X27 0x8000000
# define __0X28 0x10000000
# define __0X29 0x20000000
# define __0X30 0x40000000
# define __0X31 0x80000000
# ifndef NUM_FILTRI
# define NUM_FILTRI 14
# endif

namespace cost
 {unsigned int xmin = __0X00;
  unsigned int ymin = __0X01;
  unsigned int zmin = __0X02;
  unsigned int pxmin = __0X03;
  unsigned int pymin = __0X04;
  unsigned int pzmin = __0X05;
  unsigned int xmax = __0X06;
  unsigned int ymax = __0X07;
  unsigned int zmax = __0X08;
  unsigned int pxmax = __0X09;
  unsigned int pymax = __0X10;
  unsigned int pzmax = __0X11;
  unsigned int emin = __0X12;
  unsigned int emax = __0X13;
  unsigned int tutte[]=
   {xmin, ymin, zmin, pxmin, pymin, pzmin, xmax, ymax, zmax, pxmax, pymax, pzmax, emin, emax};
// varie ed eventuali
  }

struct _Filtro
 {
  enum class _Nomi : int
   {xmin, ymin, zmin, xmax, ymax, zmax,
    pxmin, pymin, pzmin, pxmax, pymax, pzmax,
    emin, emax} nomi;
static double * costruisci_filtro(const char *, ...);
static void individua_filtro(char *, double, double *&);
static const unsigned int cost[];
static unsigned int maschera_interna;
struct _flag_filtri
 {unsigned meno_xmin:1;
  unsigned meno_ymin:1;
  unsigned meno_zmin:1;
  unsigned piu_xmax:1;
  unsigned piu_ymax:1;
  unsigned piu_zmax:1;
  unsigned meno_pxmin:1;
  unsigned meno_pymin:1;
  unsigned meno_pzmin:1;
  unsigned piu_pxmax:1;
  unsigned piu_pymax:1;
  unsigned piu_pzmax:1;
  unsigned meno_ener:1;
  unsigned piu_ener:1;
  _flag_filtri operator=(int o)
   {meno_xmin = meno_ymin = meno_zmin =
    meno_pxmin = meno_pymin = meno_pzmin =
    piu_xmax = piu_ymax = piu_zmax =
    piu_pxmax = piu_pymax = piu_pzmax =
    meno_ener = piu_ener = 0;
    return *this;}
// varie ed eventuali
   } flag_filtri;
  static const char * descr[];
  _Filtro(double *dati, unsigned int n_dati[], double *val, unsigned int maschera = 0)
    {double * pntt_loc, p[3], E;
     unsigned int corrente = 0, tests[32];
     bool flag;
     unsigned char tot_test = 0;
     flag_filtri = 0;
     if(!maschera) maschera = maschera_interna;
     if(!maschera)
       {std :: cerr << "NON È STATO IMPOSTATO ALCUN FILTRO; NON PERDIAMO TEMPO\n";
        return;}
     for(unsigned char c=0; c < 32; ++c)
      { unsigned int r = maschera & cost[c];
        if(!r) continue;
        tests[tot_test++] = cost[c];
      }
     for(unsigned int i=0; i < n_dati[0]; ++i)
      {pntt_loc = dati + i*n_dati[1];
       flag = true;
       p[0] = pntt_loc[3], p[1] = pntt_loc[4], p[2] = pntt_loc[5], E;
       for(unsigned char c=0; c < tot_test; ++c)
         {if(!flag) break;
          if(tests[c] == __0X12 || tests[c] == __0X13)
            E = P_MASS * sqrt(p[0]*p[0]+p[1]*p[1]+p[2]*p[2]);
          switch(tests[c])
            {case __0X00: // cost::xmin
               nomi = _Nomi::xmin;
               flag_filtri . meno_xmin = pntt_loc[(int)nomi] >= val[(int)nomi];
               flag = flag && flag_filtri . meno_xmin;
             break;
             case __0X01: // cost::ymin
               nomi = _Nomi::ymin;
               flag_filtri . meno_ymin = pntt_loc[(int)nomi] >= val[(int)nomi];
               flag = flag && flag_filtri . meno_ymin;
             break;
             case __0X02: // cost::zmin
               nomi = _Nomi::zmin;
               flag_filtri . meno_zmin = pntt_loc[(int)nomi] >= val[(int)nomi];
               flag = flag && flag_filtri . meno_zmin;
             break;
             case __0X03: // cost::pxmin
               nomi = _Nomi::pxmin;
               flag_filtri . meno_pxmin = pntt_loc[(int)nomi] >= val[(int)nomi];
               flag = flag && flag_filtri . meno_pxmin;
             break;
             case __0X04: // cost::pymin
               nomi = _Nomi::pymin;
               flag_filtri . meno_pymin = pntt_loc[(int)nomi] >= val[(int)nomi];
               flag = flag && flag_filtri . meno_pymin;
             break;
             case __0X05: // cost::pzmin
               nomi = _Nomi::pzmin;
               flag_filtri . meno_pzmin = pntt_loc[(int)nomi] >= val[(int)nomi];
               flag = flag && flag_filtri . meno_pzmin;
             break;
             case __0X06: // cost::xmax
               nomi = _Nomi::xmax;
               flag_filtri . piu_xmax = pntt_loc[(int)nomi-6] <= val[(int)nomi];
               flag = flag && flag_filtri . piu_xmax;
             break;
             case __0X07: // cost::ymax
                nomi = _Nomi::ymax;
               flag_filtri . piu_ymax = pntt_loc[(int)nomi-6] <= val[(int)nomi];
               flag = flag && flag_filtri . piu_ymax;
             break;
             case __0X08: // cost::zmax
               nomi = _Nomi::zmax;
               flag_filtri . piu_zmax = pntt_loc[(int)nomi-6] <= val[(int)nomi];
               flag = flag && flag_filtri . piu_zmax;
             break;
             case __0X09: // cost::pxmax
                nomi = _Nomi::pxmax;
               flag_filtri . piu_pxmax = pntt_loc[(int)nomi-6] <= val[(int)nomi];
               flag = flag && flag_filtri . piu_pxmax;
             break;
             case __0X10: // cost::pymax
               nomi = _Nomi::pymax;
               flag_filtri . piu_pymax = pntt_loc[(int)nomi-6] <= val[(int)nomi];
               flag = flag && flag_filtri . piu_pymax;
             break;
             case __0X11: // cost::pzmax
               nomi = _Nomi::pzmax;
               flag_filtri . piu_pzmax = pntt_loc[(int)nomi-6] <= val[(int)nomi];
               flag = flag && flag_filtri . piu_pzmax;
             }
             if(tests[c] == __0X12) // cost::emin
                flag_filtri . meno_ener = E >= val[n_dati[1]],
                flag = flag && flag_filtri . meno_ener;
             if(tests[c] == __0X13)  // cost::emax
                flag_filtri . piu_ener = E <= val[n_dati[1]+1],
                flag = flag && flag_filtri . piu_ener;

          }
       if(!flag) continue;
       for(int k=0; k < n_dati[1]; ++k) dati[n_dati[1]*corrente+k] = pntt_loc[k];
       corrente++;
       }
     n_dati[0] = corrente,
     maschera_interna = 0;
     }
};

const char * _Filtro :: descr[] =
    {"xmin",
     "ymin",
     "zmin",
     "xmax",
     "ymax",
     "zmax",
     "pxmin",
     "pymin",
     "pzmin",
     "pxmax",
     "pymax",
     "pzmax",
     "Emin",
     "Emax"
// varie ed eventuali
     };

const unsigned int _Filtro :: cost[] =
{
__0X00, __0X01, __0X02, __0X03, __0X04, __0X05, __0X06, __0X07,
__0X08, __0X09, __0X10, __0X11, __0X12, __0X13, __0X14, __0X15,
__0X16, __0X17, __0X18, __0X19, __0X20, __0X21, __0X22, __0X23,
__0X24, __0X25, __0X26, __0X27, __0X28, __0X29, __0X30, __0X31
};

double * _Filtro :: costruisci_filtro(const char *p, ...)
 {va_list app;
  char * buff = new char[128], *z = buff;
  double val, *tutti_val = new double[NUM_FILTRI];
  va_start(app, p);
  strcpy(buff, p);
  do
   {
    val = va_arg(app, double);
    individua_filtro(buff, val, tutti_val);
    if(!tutti_val) return nullptr;
    z = va_arg(app, char *);
    if(!z) break;
    strcpy(buff, z);

    } while(1);
  va_end(app);
  return tutti_val;}

void _Filtro :: individua_filtro(char *b, double v, double *& V)
  {int i;
   for(i=0; i < NUM_FILTRI; ++i) if(!strcasecmp(b, descr[i])) break;
   if(i >= NUM_FILTRI) {V = nullptr; return;}
   V[i] = v;
   maschera_interna |= cost :: tutte[i];
   }

unsigned int _Filtro :: maschera_interna = 0;
/*
int main(int narg, char ** args)
 {using namespace std;

  double * dati = new double[56], // array dei dati
  val[] = {1,1,1,1,1,1,1,1,1,1,1,3,1,1}; // array ordinato delle soglie
  unsigned int N[] {8, 7},  // struttura fine del puntatore "dati"
  m = cost :: xmin | cost :: pzmax; // filtri che si vogliono applicare


  // i dati da filtrare sono presi da un file: consistono in 8 righe di 7 dati ciascuna
  ifstream issa(args[1]);
  issa . read (reinterpret_cast<char*>(dati), 56*sizeof(double));
  issa . close();


  // scrittura dei dati letti (per verifica)
  for(int i=0; i < N[0]; ++i) {for(int j=0; j < N[1]; j++) cout << dati[N[1]*i+j] << ' '; cout << '\n';}

  //applicazione del _Filtro con fornitura di TUTTI gli argomenti
  //_Filtro(dati, N, val, m);


  // oppure applicazione del _Filtro con uso di costruisci_filtro (equivalente alla precedente)
  //_Filtro(dati, N, _Filtro :: costruisci_filtro("xmin", 1.0, "xmax", 5.0, (char *)NULL));


  // oppure applicazione del _Filtro con uso di costruisci_filtro (equivalente alla precedente,
  // perché l'ORDINE DEGLI ARGOMENTI è irrilevante)
  //_Filtro(dati, N, _Filtro :: costruisci_filtro("xmax", 5.0, "xmin", 1.0, (char *)NULL));


  // oppure applicazione ERRATA del filtro (contumelia, ma "no operation")
  _Filtro(dati, N, _Filtro :: costruisci_filtro("MERDE", 1.0, "PUPU", 5.0, (char *)NULL));


  // all'uscita in "dati", a partire dall'inizio, sopravvivono N[0] particelle
  cout << "sopravvissute " << N[0] << " particelle\n";
  for(int i=0; i < N[0]; ++i) {for(int j=0; j < N[1]; j++) cout << dati[N[1]*i+j] << ' '; cout << '\n';}
  }
*/