import bokeh as bk
import bokeh.plotting as bkp
from bokeh.embed import components
from bokeh.models import ColumnDataSource, RangeTool
from bokeh.layouts import column
from bokeh.io import curdoc
import numpy as np
import pandas as pd


def init_couleur_et_noms():
    init_cols = ['demande', 'electrolyse',
            'prodOffshore', 'prodOnshore', 'prodPV', 'rivprod', 'lakeprod',
            'Bprod', 'Bstored', 'Bcons',
            'Gprod', 'Gstored', 'Gcons',
            'Lprod', 'Lstored',
            'Nprod', 'Nstored',
            'Sprod', 'Sstored', 'Scons',
            'prodResiduelle', '-prodResiduelle',
            's', 'p'
            ]
    init_couls = ["black", "grey",
                "seagreen", "yellowgreen", "yellow", "aquamarine", "blue",
                "orange", "orange", "green",
                "purple", "purple", "grey",
                "darkblue", "darkblue",
                "coral", "coral",
                "lightblue", "lightblue", "lightblue",
                "darkslategray", "darkslategray",
                "blue", "red"
                ]
    init_noms = [
        'demande', 'electrolyse',
        'prodOffshore', 'prodOnshore', 'prodPV', 'rivprod', 'lakeprod',
        'Batt-', 'Bstored', 'Batt+',
        'Gaz2power', 'Gaz stock', 'Power2Gaz',
        'Lprod', 'Lstored',
        'Nprod', 'Nstored',
        'Step-', 'Stock Step', 'Step+',
        'prodResiduelle', '-prodResiduelle',
        'surplus', "pénuries"
    ]

    couleurs = {}
    noms = {}

    i=0
    for col in init_cols:
        couleurs[col] = init_couls[i]
        noms[col] = init_noms[i]
        i += 1

    couleurs = pd.Series(couleurs)
    noms = pd.Series(noms)
    return init_cols, couleurs, noms


colonnes, couleurs, noms = init_couleur_et_noms()


class Visualiseur:

    def __init__(self, chroniques, data_mix="./data_mix/"):
        self.data_mix = data_mix
        self.figs = {}
        chroniques['demande+P2G'] = chroniques["demande"] + chroniques["Gcons"]
        chroniques['prod_non_pilot'] = chroniques[['prodOffshore', 'prodOnshore', 'prodPV', 'rivprod']].sum(axis=1)
        chroniques['prod_pilot'] = chroniques[["Nprod", "Lprod", "Gprod"]].sum(axis=1)
        chroniques['demandeRésiduelle'] = -chroniques["prodResiduelle"] + chroniques["Gcons"]
        chroniques['demandeStock'] = chroniques['demandeRésiduelle'] - chroniques["prod_pilot"]

        self.chroniques = chroniques
        self.source = bk.models.ColumnDataSource(chroniques)

        self.dates = np.array(chroniques['date'], dtype=np.datetime64)

    def get_dates_et_source(self):
        return self.dates, self.source

    def set_fig(self, fig=bkp.figure(), titre="vierge"):
        self.figs[titre] = fig

    def set_figs(self):
        self.set_fig()

    def get_composants(self):
        script, divs = components(self.figs)
        return {"script": script, "divs": divs}

    def cumul_plot(self, cols, fig=bkp.figure(x_axis_type="datetime")):
        fig.varea_stack(stackers=cols, x="date", color=couleurs[cols].to_list(),
                        legend_label=noms[cols].to_list(), source=self.source)
        fig.legend.click_policy = "mute"
        return fig

    def range_fig(self, deb=24 * 31, fin=24 * 31 + 24 * 7):
        p = bkp.figure(height=300, width=800, tools="xpan", toolbar_location=None,
                       x_axis_type="datetime", x_axis_location="above",
                       background_fill_color="#efefef", x_range=(self.dates[deb], self.dates[fin]))

        select = bkp.figure(title="Déplacez le milieu ou un bord du rectangle",
                            height=130, width=800, y_range=p.y_range,
                            x_axis_type="datetime", y_axis_type=None,
                            tools="", toolbar_location=None, background_fill_color="#efefef")

        range_tool = RangeTool(x_range=p.x_range)
        range_tool.overlay.fill_color = "navy"
        range_tool.overlay.fill_alpha = 0.2

        select.ygrid.grid_line_color = None
        select.add_tools(range_tool)
        return p, select

    def show(self, fig):
        bkp.show(fig)
class vScenario(Visualiseur):

    def set_fig_1(self):
        fich = "S1_25-50.csv"
        df = pd.read_csv(self.data_mix + fich)

    def set_figs(self):
        fig = self.cumul_plot(cols=['demande', 'electrolyse'])
        self.set_fig(fig, "Scenario")


class vProduction(Visualiseur):

    def fig_prod(self):
        from bokeh.palettes import tol

        p, select = self.range_fig()
        non_pilot = ['rivprod',  'prodOffshore', 'prodOnshore', 'prodPV']
        pilot = ["Nprod", 'Lprod', "Gprod", "Bprod", "Sprod"]
        p = self.cumul_plot(cols=["Gcons", "Nprod", 'rivprod', 'prodOffshore', 'Lprod', "Gprod", 'prodOnshore', 'prodPV'], fig=p)
        p.line(x='date', y='demande+P2G', source=self.source, legend_label='demande + P2G')
        p.line(x='date', y='demande', source=self.source, legend_label=noms['demande'])
        p.yaxis.axis_label = 'production (GW)'
        p.legend.click_policy = "mute"


        n = bkp.figure(height=300, width=800, tools="xpan", toolbar_location=None,
                       x_axis_type="datetime", x_axis_location="above",
                       background_fill_color="#efefef", x_range=p.x_range)

        n = self.cumul_plot(cols=pilot, fig=n)
        n.line('date', 'demandeRésiduelle', source=self.source, legend_label="demande + P2G- non pilotable")
        n.yaxis.axis_label = 'production (GW)'
        n.legend.click_policy = "mute"

        stock = [ "Bcons", "Bprod", "Scons", "Sprod",  "Gprod", "s",  "p",]
        s = bkp.figure(height=300, width=800, tools="xpan", toolbar_location=None,
                       x_axis_type="datetime", x_axis_location="above",
                       background_fill_color="#efefef", x_range=p.x_range)
        s = self.cumul_plot(cols=stock, fig=s)
        s.line('date', 'demandeStock', source=self.source, legend_label="demande restante G+B+S")
        s.yaxis.axis_label = 'production (GW)'
        s.legend.click_policy = "mute"

        select.line('date', 'demande', source=self.source)
        fig = column(p, n, s, select)
        return fig

    def fig_penuries(self):
        from bokeh.palettes import tol

        p, select = self.range_fig()

        cols = ["s", "p"]

        p = self.cumul_plot(cols, p)
        p.line(x='date', y='demandeRésiduelle', source=self.source, legend_label='production résiduelle')
        p.yaxis.axis_label = 'surplus penuries (GW)'
        p.legend.click_policy = "mute"

        select.line('date', 'demandeRésiduelle', source=self.source)
        fig = column(p, select)
        return fig

    def set_figs(self):
        fig = self.fig_prod()
        self.set_fig(fig, "production")
        self.set_fig(self.fig_penuries())


vuesClasses = {"resultats": Visualiseur,
               "scenario": vScenario,
               "production": vProduction
               }

if __name__ == "__main__":
    from flaskapp import archiveur
    import os
    chemin = os.path.dirname(os.path.realpath(__file__))
    dataPath = chemin + "/../flaskapp/"
    dm = archiveur.DataManager(equipe="winn", partie="S1", chemin=dataPath)

    chroniques = dm.get_chroniques()
    resultats = dm.get_results()
    chroniques.describe()
    self = vProduction(chroniques)
    bkp.show(self.fig_prod())
#    self.set_figs()
#    composants = self.get_composants()
#    print(composants["divs"])
