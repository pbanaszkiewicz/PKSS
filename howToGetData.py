#po odpaleniu tego pliku, pod warunkiem ze w sciezce data/ex6.txt znaduje
#sie poprawny plik, wyswietli nam sie wektor czasu zarejestrowany
#podczas eksperymentu.

#potrzebna biblioteka
import ast

#otwieramy wybrany plik
file = open('data/ex6.txt','r')

#zapisujemy zawartosc pliku do listy fileContent
#1 element listy = 1 linia z pliku
fileContent = file.readlines()

#tworzymy liste na dana, ktora chcemy odczytac z pliku
myData = []

#dla kazdej linii z pliku...
for line in fileContent:
  #do zmiennej temp wpisuje 'doslowna ewaluacje', czyli interpretuje
  #string z pliku jak linie pythona. W ten sposob w zmiennej 'temp' 
  #znajduje sie zmienna typu slownik dla danej linii.
  temp = ast.literal_eval(line)
  
  #do listy zawierajacej moja dana wpisuje jej wartosc ze slownika.
  #w tym przykladzie pobieram wartosci zmiennej 'time'
  myData.append(temp['time'])

#po zakonczeniu petli w liscie myData znajduje sie wektor danych  
print myData

#eksport do .txt np. dla Matlaba
matlabFile = open('data/example.txt','w')
for i in myData:
  matlabFile.write(str(i))
  matlabFile.write('\n')
  
#CO DALEJ W MATLABIE Z TYM?
#A TYLE:
#   fileID = fopen('data\example.txt','r');
#   A = fscanf(fileID,'%d')  %'%f' jesli czytamy float!!!
#   %i mamy iscie piekny wektor
