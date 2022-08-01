# -*- coding: utf8 -*-
import csv
import os
import subprocess
import sys
import pandas as pd
import webbrowser
from PyQt5.QtCore import  *
from PyQt5.QtWidgets import * #QDialog, QLabel, QLineEdit, QPushButton, QGridLayout, QFileDialog, QMessageBox, QWidget, QApplication


class Ogr_exe(QDialog):
    def __init__(self, parent=None):
        super(Ogr_exe, self).__init__(parent)
        self.interfejs_pocz()
               
    def interfejs_pocz(self):
        self.resize(300, 200)
        self.setWindowTitle("Wprowadź aplikację ogr2ogr!")
        
        # etykiety
        etykieta_ogr1 = QLabel(" Program do działania wymaga dostępu do narzędzia <b>ogr2ogr.exe</b>. ", self)
        etykieta_ogr1.setStyleSheet("font-size: 11.5pt")
        
        etykieta_ogr2 = QLabel("Wskaż lokalizację pliku ogr2ogr.exe. Znajdziesz go w folderze QGIS\\bin.")
        etykieta_ogr2.setStyleSheet("font-size: 11.5pt")
        
        # pole edycji
        self.pole_ogr = QLineEdit()
        self.pole_ogr.setEnabled(False)
        self.pole_ogr.setStyleSheet("color: black; background-color: white;")
        
        #przyciski
        btn_ogr = QPushButton('Wybierz',self)
        btn_ogr.setToolTip('Kliknij, aby wybrać')
        btn_ogr.move(100, 70)
        btn_ogr.clicked.connect(self.ogr2ogr)

        self.btn_dalej = QPushButton('Dalej', self)
        self.btn_dalej.setToolTip('Dalej')
        self.btn_dalej.move(50, 70)
        self.btn_dalej.setEnabled(False)
        self.btn_dalej.clicked.connect(self.okno_glowne)
        
        uklad2 = QGridLayout()
        uklad2.addWidget(etykieta_ogr1)
        uklad2.addWidget(etykieta_ogr2)
        uklad2.addWidget(self.pole_ogr,2,0)
        uklad2.addWidget(btn_ogr,2,2)
        uklad2.addWidget(self.btn_dalej)

        # przypisanie ukladu do okna
        self.setLayout(uklad2)

        self.show()
        
    @pyqtSlot()
    def ogr2ogr(self):
        dialog = QFileDialog(self)
        self.wyb_ogr = dialog.getOpenFileName()
        self.app_exe = str(self.wyb_ogr).split("'")[1]
        self.pole_ogr.setText(self.app_exe)        
        
        if self.app_exe.endswith("ogr2ogr.exe"):
            self.btn_dalej.setEnabled(True)
        else:
            msg_exe = QMessageBox()
            msg_exe.critical(self,'BŁĄD','Użyto błędnej aplikacji!')
            self.btn_dalej.setEnabled(False)
            
        self.dalej = App(wybrany_ogr = self.app_exe)
        
    def okno_glowne(self):   
        self.dalej.show()
        self.hide()
    
class App(QWidget):
    def __init__(self, parent=None, wybrany_ogr = None):
        super(App, self).__init__(parent)
        self.ogr2ogr = wybrany_ogr
        self.interfejs()
        
    def interfejs(self):  
        
            #Okno główne
        self.resize(1000, 300)
        self.setWindowTitle("Porównaj bazy!")
            
            # etykiety
        etykieta1 = QLabel("Baza TERYT: ", self)
        etykieta2 = QLabel("Baza PRG: ", self)  
        
            # pole edycji
        self.pole_teryt = QLineEdit()
        self.pole_teryt.setEnabled(False)
        self.pole_teryt.setStyleSheet("color: black; background-color: white;")
            
        self.pole_prg = QLineEdit()
        self.pole_prg.setEnabled(False)
        self.pole_prg.setStyleSheet("color: black; background-color: white;")

            # przyciski
        self.button_teryt = QPushButton('Wybierz', self)
        self.button_teryt.setToolTip('Wybierz folder z bazą TERYT')
        self.button_teryt.move(100, 70)
        self.button_teryt.clicked.connect(self.on_click_teryt)
        
        self.button_prg = QPushButton('Wybierz', self)
        self.button_prg.setToolTip('Wybierz folder z bazą PRG')
        self.button_prg.move(100, 70)
        self.button_prg.clicked.connect(self.on_click_prg)
        
        self.btn_porownaj = QPushButton('Porównaj bazy', self)
        self.btn_porownaj.setToolTip('Kliknij i porównaj obie bazy')
        self.btn_porownaj.move(100, 70)
        self.btn_porownaj.setEnabled(False)
        self.btn_porownaj.clicked.connect(self.porownaj)

        btn_pomoc = QPushButton('POMOC', self)
        btn_pomoc.setToolTip('Nie wiesz skąd wziąć bazy? Zajrzyj tutaj!')
        btn_pomoc.move(30, 70)
        btn_pomoc.clicked.connect(self.pomoc)

            # uporzadkowanie widzetow do ukladu
        uklad = QGridLayout()
        uklad.addWidget(etykieta1, 0, 0)
        uklad.addWidget(self.pole_teryt, 0, 1)
        uklad.addWidget(self.button_teryt, 0, 2)
        uklad.addWidget(etykieta2, 2, 0)
        uklad.addWidget(self.pole_prg, 2, 1)
        uklad.addWidget(self.button_prg, 2, 2)
        uklad.addWidget(self.btn_porownaj, 3, 1)
        uklad.addWidget(btn_pomoc,3,2)

            # przypisanie ukladu do okna
        self.setLayout(uklad)

        #self.show()
        
    def pomoc(self):
        pomocBox = QMessageBox()
        pomocBox.setWindowTitle('Skąd wziąć bazy?')
        pomocBox.setText('Jeżeli nie posiadasz na swoim dysku baz lub nie wiesz skąd je pozyskać,\
                        skorzystaj z poniższych opcji i pobierz je ze stron. \
                        Kliknięcie w przycisk przeniesie Cię do odpowiedniej witryny. Pamiętaj, aby rozpakować pobrane foldery!\
                        <ul>Do pobrania:\
                            <li> Baza TERYT: wersje danych: adresowa; dane: ULIC </li>\
                            <li> Baza PRG: PRG-punkty adresowe i ulice; rozszerzenie *.GML </li>   \
                        <ul>')
        
        pomocBox.setStandardButtons(QMessageBox.Cancel | QMessageBox.Yes | QMessageBox.No)
        pomocBox.setDefaultButton(QMessageBox.Cancel)
        cancel = pomocBox.button(QMessageBox.Cancel)
        cancel.setText("Anuluj")
        pomoc_teyrt = pomocBox.button(QMessageBox.Yes)
        pomoc_teyrt.setText('TERYT')
        pomoc_prg = pomocBox.button(QMessageBox.No)
        pomoc_prg.setText('PRG')
        pomocBox.exec_()
        
        if pomocBox.clickedButton() == pomoc_teyrt:
            webbrowser.open('https://eteryt.stat.gov.pl/eTeryt/rejestr_teryt/udostepnianie_danych/baza_teryt/uzytkownicy_indywidualni/pobieranie/pliki_pelne.aspx?contrast=default')
        elif pomocBox.clickedButton() == pomoc_prg:
            webbrowser.open('http://www.gugik.gov.pl/pzgik/dane-bez-oplat/dane-z-panstwowego-rejestru-granic-i-powierzchni-jednostek-podzialow-terytorialnych-kraju-prg')     

    @pyqtSlot()
    def on_click_teryt(self):
        try:
            dialog = QFileDialog(self)
            self.wyb_folder_teryt = dialog.getExistingDirectory()
            self.pole_teryt.setText(self.wyb_folder_teryt)
            
            if (self.wyb_folder_teryt != None and self.wyb_folder_prg != None):
                self.btn_porownaj.setEnabled(True)
        except AttributeError:
            pass
        
    @pyqtSlot()
    def on_click_prg(self):
        try:
            dialog = QFileDialog(self)
            self.wyb_folder_prg = dialog.getExistingDirectory()
            self.pole_prg.setText(self.wyb_folder_prg)  
            
            if (self.wyb_folder_teryt != None and self.wyb_folder_prg != None):
                self.btn_porownaj.setEnabled(True)
        except AttributeError:
            pass                     
    def porownaj(self):
        self.hide()
        progress = QProgressDialog()
        progress.setFixedWidth(400)
        progress.setWindowTitle('Porównanie baz')
        progress.setLabelText("Trwa porównywanie baz...")
        progress.setMinimum(0)
        progress.setMaximum(100)
        progress.setAutoClose(True)
        progress.setCancelButton(None)
        QApplication.processEvents()
        progress.show()
        QApplication.processEvents()

        folder_prg = self.wyb_folder_prg   #wybrany przez użytkownika

        files_dict = {}
        progress.setValue(0)
        QApplication.processEvents()
        
        try:
            QApplication.processEvents()
            progress.setValue(10)
            for nazwa_pliku in os.listdir(folder_prg):
                # konwertuje gml na csv
                if nazwa_pliku.endswith('.xml'):
                    plik_pelna_sciezka = os.path.join(folder_prg, nazwa_pliku)

                    nazwa1 = nazwa_pliku.replace('.xml', '_1.csv')
                    nazwa2 = nazwa_pliku.replace('.xml', '_2.csv')
                    nazwa3 = nazwa_pliku.replace('.xml', '_3.csv')

                    output1 = os.path.join(folder_prg, nazwa1)
                    output2 = os.path.join(folder_prg, nazwa2)
                    output3 = os.path.join(folder_prg, nazwa3)

                    sql1 = "SELECT idTERYT,nazwa FROM PRG_JednostkaAdministracyjnaNazwa"
                    sql2 = "SELECT idTERYT,nazwa FROM PRG_MiejscowoscNazwa"
                    sql3 = "SELECT idTERYT,przedrostek1Czesc,przedrostek2Czesc,nazwaCzesc,nazwaGlownaCzesc FROM PRG_UlicaNazwa "  

                    command1 = [self.ogr2ogr, "-f", "CSV", output1, plik_pelna_sciezka,
                                "-lco", "SEPARATOR=SEMICOLON", "-sql", sql1]
                    
                    command2 = [self.ogr2ogr, "-f", "CSV", output2, plik_pelna_sciezka,
                                "-lco", "SEPARATOR=SEMICOLON", "-sql", sql2]
                    
                    command3 = [self.ogr2ogr, "-f", "CSV", output3, plik_pelna_sciezka,
                                "-lco", "SEPARATOR=SEMICOLON", "-sql", sql3]

                    
                    QApplication.processEvents()
                    subprocess.run(command1)
                    QApplication.processEvents()
                    subprocess.run(command2)
                    QApplication.processEvents()
                    subprocess.run(command3)
                    progress.setValue(15)                
                    QApplication.processEvents()
                    
                    
            # łączy 1 z 1, 2 z 2, 3 z 3
            for nazwa_pliku in os.listdir(folder_prg):
                if nazwa_pliku.endswith('.csv'):
                    if os.path.splitext(nazwa_pliku)[0][-2:] in files_dict.keys():
                        files_dict[os.path.splitext(nazwa_pliku)[0][-2:]].append(
                            os.path.join(folder_prg, nazwa_pliku))
                    else:
                        files_dict[os.path.splitext(nazwa_pliku)[0][-2:]] = [
                            os.path.join(folder_prg, nazwa_pliku)]
                        
            QApplication.processEvents()
            progress.setValue(20)
            
            for file_list in files_dict.keys():
                combined_csv = pd.concat(
                    [pd.read_csv(file, header=None, error_bad_lines=False) for file
                    in files_dict[file_list]])
                combined_csv.head()
              
                QApplication.processEvents()
                
                combined_csv.to_csv(os.path.join(folder_prg, f"out{file_list}.csv"),
                                    quotechar='"', quoting=csv.QUOTE_ALL,
                                    index=False, encoding='utf-8')
  
            QApplication.processEvents()
            progress.setValue(25)

            # łączy pliki w DataFrame
            plik1 = pd.read_csv(os.path.join(folder_prg, "out_1.csv"), 'r',
                                encoding='utf-8', delimiter=';', index_col=None)
            plik2 = pd.read_csv(os.path.join(folder_prg, "out_2.csv"), 'r',
                                encoding='utf-8', delimiter=';', index_col=None)
            plik3 = pd.read_csv(os.path.join(folder_prg, "out_3.csv"), 'r',
                                encoding='utf-8', delimiter=';', index_col=None)
            #progress.setValue(66)
            
            plik = open(os.path.join(folder_prg, "baza_PRG.csv"), mode='a+',
                        encoding='utf-8')

            df1 = pd.DataFrame(plik1)
            df2 = pd.DataFrame(plik2)
            df3 = pd.DataFrame(plik3)
            
            QApplication.processEvents()
            progress.setValue(30)
            
            merge_all = pd.concat([df1, df2, df3], axis=1)

            merge_all.head()
            # print(merge_all)

            # eksport dataFrame do csv
            merge_all.to_csv(plik, sep=';', encoding='utf-8')

            plik.close()

            QApplication.processEvents()
            progress.setValue(35)
            # ===================================================================================================================
            # --------------------------------------- U S U W A   Z B E D N E   P L I K I ---------------------------------------

            for nazwa_pliku in os.listdir(folder_prg):
                QApplication.processEvents()
                if (nazwa_pliku.endswith("_1.csv") or nazwa_pliku.endswith("_2.csv") or nazwa_pliku.endswith("_3.csv")):
                    usuwany_plik = nazwa_pliku
                    os.remove(os.path.join(folder_prg, usuwany_plik))
                else:
                    continue
            
            QApplication.processEvents()
            progress.setValue(45)
        
        except FileNotFoundError:
            zamknij = QMessageBox()
            zamknij.setWindowTitle('Wystąpił nieoczekiwany błąd')
            zamknij.setText('Coś poszło nie tak. W wybranych folderach nie znaleziono odpowiednich plików.Program kończy działanie! Uruchom go ponownie, aby porównać bazy adresowe.')   
            zamknij.setStandardButtons(QMessageBox.Ok)
            ok = zamknij.button(QMessageBox.Ok)
            ok.setText('Zakończ')
            zamknij.exec_()
            
        except AttributeError:
            zamknij = QMessageBox()
            zamknij.setWindowTitle('Wystąpił nieoczekiwany błąd')
            zamknij.setText('Coś poszło nie tak. Nie ustawiono w polach żadnych folderów.Program kończy działanie! Uruchom go ponownie, aby porównać bazy adresowe.')   
            zamknij.setStandardButtons(QMessageBox.Ok)
            ok = zamknij.button(QMessageBox.Ok)
            ok.setText('Zakończ')
            zamknij.exec_()
            
     # ================================================================================================================

        folder_teryt = self.wyb_folder_teryt
        
        
        for nazwa_pliku in os.listdir(folder_teryt):
            if nazwa_pliku.endswith('.csv'):        
                self.TERYT = nazwa_pliku

        
        self.TERYT = os.path.join(folder_teryt,self.TERYT)
        TERYT = self.TERYT
                
        self.plik =  os.path.join(folder_prg, "baza_PRG.csv")
        #plik = self.plik
                
        gminy = []
        miejscowosci = []
        ulice = []
        prg = []
        prg_ulice_dict = {}
        self.errorsList=[]

        QApplication.processEvents()
        progress.setValue(55)

        with open(self.plik, mode='r', encoding='utf-8') as prg_file:
            prgReader = csv.reader(prg_file, delimiter=';')
            fields = next(prgReader)
            print(fields)
            
            QApplication.processEvents()
            progress.setValue(60)
            
            try:
                for row in prgReader:
                    # prg.append(row)
                    for e in row:
                        identyfikator = e.split(';')[0]
                        # print(e)
                        prg.append(identyfikator)
                        #identyfikator1 = e.split(';')[1:]

                        ulica_prg = row[3]
                        id_ulicy_prg = ulica_prg.split(';')[0]
                        rodzaj = ulica_prg.split(';')[1]
                        if rodzaj == '':
                            rodzaj = 'ul. '
                        
                        czesc1 = ulica_prg.split(';')[2]
                        czesc2 = ulica_prg.split(';')[3]
                        czescGlowna = ulica_prg.split(';')[4]
                        
                        nazwa_ulicy_prg = rodzaj + ' ' + czesc1 +  ' ' + czesc2 + ' ' + czescGlowna
                        
                        nazwa_ulicy_prg = nazwa_ulicy_prg.replace('   ',' ')
                        nazwa_ulicy_prg = nazwa_ulicy_prg.replace('  ',' ')
                        nazwa_ulicy_prg = nazwa_ulicy_prg.strip()

                        prg_ulice_dict[id_ulicy_prg] = nazwa_ulicy_prg
                        
                        QApplication.processEvents()
                        progress.setValue(70)
            except IndexError:
                pass
        print(prg)
        #print(prg_ulice_dict)

        QApplication.processEvents()
        progress.setValue(85)
        
        teryt_ulice_dict = {}
        
        with open(TERYT, mode='r', encoding='utf-8') as teryt_file:
            terytReader = csv.reader(teryt_file, delimiter=';')
            fields = next(terytReader)
            # print(fields)

            QApplication.processEvents()
            progress.setValue(90)    
            try:
                for teryt in terytReader:
                    # woj_teryt + pow_teryt + gmina_teryt
                    woj = teryt[0]
                    if (woj.startswith('0')):
                        woj = teryt[0][1]
                    else:
                        woj = teryt[0]

                    id_gmina_teryt = woj + teryt[1] + teryt[2] + teryt[3]
                
                    # print(id_gmina_teryt)
                    gminy.append(id_gmina_teryt)

                    QApplication.processEvents()

                    # miejscowosc
                    id_miejsowosc_teryt = teryt[4]
                    miejscowosci.append(id_miejsowosc_teryt)
                        
                    QApplication.processEvents()
                        
                    # ulice
                    id_ulice_teryt = teryt[5]
                    ulice.append(id_ulice_teryt)
                    nazwa_ulice_teryt = teryt[6] + ' ' + teryt[8] + ' ' + teryt[7]
                
                    nazwa_ulice_teryt = nazwa_ulice_teryt.replace('  ',' ')
                    nazwa_ulice_teryt = nazwa_ulice_teryt.replace('   ',' ')
                    nazwa_ulice_teryt = nazwa_ulice_teryt.strip()                  
                    
                    teryt_ulice_dict[id_ulice_teryt] = nazwa_ulice_teryt
                
            except IndexError:
                pass
                
            QApplication.processEvents()
            progress.setValue(92)   
        
        print(
            '-------------------------------------------------------------------------------------------------------------------------------------')
        # ----------------------------------------------------------------------gminy      
        for i in gminy:
            QApplication.processEvents()
            try:
                if i == prg.index(i):
                    True #znaleziono.append(i)          
            except ValueError:
                if(len(i)==6):
                    i = "0"+i

                blad = 'Brak gminy o numerze ID: ' + i
                self.errorsList.append(blad)
                
        QApplication.processEvents()
        progress.setValue(94)            
            #----------------------------------------------------------------------miejscowosci    
        for i in miejscowosci:
            QApplication.processEvents() 
            try:
                if i == prg.index(i):
                    True #znaleziono.append(i)
            except ValueError:
                blad = ('Brak miejscowości o numerze ID: ' + i)
                self.errorsList.append(blad)
        
        QApplication.processEvents()
        progress.setValue(96)                
            #----------------------------------------------------------------------ulice   
        for key in teryt_ulice_dict: 
            try:
                if teryt_ulice_dict.keys() != prg_ulice_dict.keys():
                    #znaleziono.append(teryt_ulice_dict.keys())          
                        if teryt_ulice_dict[key] == prg_ulice_dict[key]:
                                    True #znaleziono.append(teryt_ulice_dict[key])
                        else:
                            blad = ('Błąd w zapisie nazwy ulicy: ' + prg_ulice_dict[key] + ', ID ulicy: ' + key + '. Poprawna nazwa: ' + teryt_ulice_dict[key])      
                            self.errorsList.append(blad)
            except KeyError:
                blad = ('Brak ulicy o numerze ID: ' + key)
                self.errorsList.append(blad)
        
                       
        QApplication.processEvents()
        progress.setValue(98)
                
        self.errorsList = list(set(self.errorsList))
        
        QApplication.processEvents()
        progress.setValue(100)
        
        progress.close()
        self.start_error_dialog()

    def start_error_dialog(self):
        self.error_dlg = Porownanie(errors = self.errorsList, plik=self.plik, TERYT=self.TERYT)
        #self.error_dlg.exec_()


class Porownanie(QDialog):
    def __init__(self, parent=None,errors=None,plik=None,TERYT = None):
        super(Porownanie, self).__init__(parent)
        self.errorsList = errors
        self.plik = plik
        self.TERYT= TERYT
        self.interfejs3()
        

    def interfejs3(self):
        self.resize(600, 400)
        self.setWindowTitle("Porównanie!")

        etykieta = QLabel("Błędy: ", self)

        tekst = self.tekst_porownania = QTextEdit()
        tekst.setGeometry(50, 0, 550, 350)
        tekst.setStyleSheet("color: black; background-color: white;")
        tekst.setReadOnly(True)
        tekst.setText(" \n".join(self.errorsList))


        eksportuj_btn = QPushButton('Eksportuj do...', self)
        eksportuj_btn.move(100, 70)
        
        zamknij_btn = QPushButton('Zakończ!', self)
        zamknij_btn.move(100, 70)
        
        
        if self.errorsList == []:
            eksportuj_btn.setEnabled(False)
        else:
            eksportuj_btn.setEnabled(True)           
        
        eksportuj_btn.clicked.connect(self.zapisz_do)
        zamknij_btn.clicked.connect(self.zakoncz)

        uklad = QGridLayout()
        uklad.addWidget(etykieta)
        uklad.addWidget(tekst)
        uklad.addWidget(eksportuj_btn)
        uklad.addWidget(zamknij_btn)
        self.setLayout(uklad)
        
        self.show()
    
    def zakoncz(self):
        sys.exit('zamknieto')
        
    def zapisz_do(self):
        try:
            file_dialog = QFileDialog(self)
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            filter = "Text Files (*.txt);;Word Document (*.doc)"
            roznice = file_dialog.getSaveFileName(self,
                                                    "Zapisywanie do pliku",
                                                    "",filter,
                                                    options=options)
            
            self.roznice_wynik = open(str(roznice).split("'")[1], mode='w', encoding='utf-8')
            print(self.roznice_wynik)      
            
            for element in self.errorsList:
                self.roznice_wynik.write(element+'\n')

            self.roznice_wynik.close()
            
            msg_zapis = QMessageBox()
            msg_zapis.information(self,'Zapisano plik','Zapisano plik pomyślnie!')
        except FileNotFoundError:
            pass
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    okno = Ogr_exe()
    sys.exit(app.exec_())