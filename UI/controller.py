import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []

    def fillDD(self):
        self._listCountry = self._model.getNazioni()
        for country in self._listCountry:
            self._view.ddcountry.options.append(ft.dropdown.Option(country))
        self._listYear = self._model.getAnni()
        for year in self._listYear:
            self._view.ddyear.options.append(ft.dropdown.Option(year))

    def handle_graph(self, e):
        self._view.txt_result.controls.clear()
        self._model.buildGraph(self._view.ddcountry.value, self._view.ddyear.value)
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        self._view.txt_result.controls.append(ft.Text(f"Vertici: {self._model.getNumNodes()}"))
        self._view.txt_result.controls.append(ft.Text(f"Archi: {self._model.getNumEdges()}"))
        self._view.update_page()

    def handle_volume(self, e):
        tupla = self._model.calcolaVolume()
        for t in tupla:
            self._view.txtOut2.controls.append(ft.Text(f"{t[0].Retailer_name} --> {t[1]}"))
        self._view.update_page()


    def handle_path(self, e):
        valore = self._view.txtN.value
        if valore == "":
            self._view.txt_result.controls.txtOut3.clear()
            self._view.txt_result.controls.txtOut3.append(ft.Text("Inserire un numero."))
            return

        try:
            N = int(valore)
        except ValueError:
            self._view.txt_result.controls.txtOut3.clear()
            self._view.txt_result.controls.txtOut3.append(ft.Text("Inserire un intero."))
            return

        if N >= 2:
            percorso, peso = self._model.getPercorso(N)
        else:
            self._view.txt_result.controls.txtOut3.clear()
            self._view.txt_result.controls.txtOut3.append(ft.Text("Inserire un numero uguale o maggiore a 2."))
            return

        self._view.txt_result.controls.txtOut3.clear()

        for p1 in percorso:
            for p2 in percorso:
                if p1 != p2:
                    self._view.txt_result.controls.txtOut3.append(ft.Text(f"{p1.Retailer_name} --> {p2.Retailer_name}: {self._model.getPeso(p1, p2)}"))
        self._view.update_page()