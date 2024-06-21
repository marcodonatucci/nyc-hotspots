import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._selected_location = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self.options = []

    def handle_hello(self, e):
        name = self._view.txt_name.value
        if name is None or name == "":
            self._view.create_alert("Inserire il nome")
            return
        self._view.txt_result.controls.append(ft.Text(f"Hello, {name}!"))
        self._view.update_page()

    def fillDDProvider(self):
        if self.options:
            self._view._ddProvider.options = self.options
        else:
            providers = self._model.get_providers()
            self.options = list(map(lambda x: ft.dropdown.Option(x), providers))
            self._view._ddProvider.options = self.options
        self._view.update_page()

    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()
        d = self._view._txtInDistanza.value
        p = self._view._ddProvider.value
        if p is None:
            self._view.txt_result.controls.append(ft.Text("Inserisci un provider!", color='red'))
            self._view.update_page()
            return
        if d is None or d == '':
            self._view.txt_result.controls.append(ft.Text("Inserisci una soglia!", color='red'))
            self._view.update_page()
            return
        try:
            d = float(d)
        except ValueError:
            self._view.txt_result.controls.append(ft.Text("Inserisci una soglia in formato numerico!", color='red'))
            self._view.update_page()
            return
        flag = self._model.buildGraph(p, d)
        if flag:
            self._view.txt_result.controls.append(ft.Text(self._model.getGraphDetails()))
            self._view._ddTarget.options.clear()
            nodi = self._model.get_nodes()
            for n in nodi:
                self._view._ddTarget.options.append(ft.dropdown.Option(text=n.Location, data=n, on_click=self.readDDTarget))
            self._view.update_page()
            return
        else:
            self._view.txt_result.controls.append(ft.Text("Errore nella creazione del grafo!", color='red'))
            self._view.update_page()
            return

    def handleAnalisi(self, e):
        self._view.txt_result.controls.clear()
        if len(self._model.graph.nodes) == 0:
            self._view.txt_result.controls.append(ft.Text("Crea un grafo!", color='red'))
            self._view.update_page()
            return
        result = self._model.analyze()
        if len(result)>0:
            for r in result:
                self._view.txt_result.controls.append(ft.Text(f"{r[0]}, numero di vicini: {r[1]}"))
            self._view.update_page()
            return
        else:
            self._view.txt_result.controls.append(ft.Text("Errore durante l'analisi!", color='red'))
            self._view.update_page()
            return

    def handleGetPercorso(self, e):
        self._view.txt_result.controls.clear()
        if len(self._model.graph.nodes) == 0:
            self._view.txt_result.controls.append(ft.Text("Creare un grafo!", color='red'))
            self._view.update_page()
            return
        if self._selected_location is None:
            self._view.txt_result.controls.append(ft.Text("Selezionare una località!", color='red'))
            self._view.update_page()
            return
        if self._model.locations is None:
            self._view.txt_result.controls.append(ft.Text("Analizzare il grafico!", color='red'))
            self._view.update_page()
            return
        if self._view._txtInStringa.value is None or self._view._txtInStringa.value == '':
            self._view.txt_result.controls.append(ft.Text("Inserire una stringa!", color='red'))
            self._view.update_page()
            return
        componenti = self._model.getPath(self._selected_location, str(self._view._txtInStringa.value))
        if componenti:
            for c in componenti:
                self._view.txt_result.controls.append(ft.Text(f"{c}"))
            self._view.update_page()
            return
        else:
            self._view.txt_result.controls.append(ft.Text("Nessun percorso trovato!", color='red'))
            self._view.update_page()
            return

    def readDDTarget(self, e):
        if e.control.data is None:
            self._selected_location = None
        else:
            self._selected_location = e.control.data
