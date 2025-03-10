import bokeh as bk
import bokeh.plotting as bkp
from bokeh.embed import components
from bokeh.models import ColumnDataSource, RangeTool
from bokeh.layouts import column
from bokeh.io import curdoc
import numpy as np
import pandas as pd

from bokeh.resources import INLINE
import flaskapp.journal.journal as jr

from flaskapp.maitre_de_jeu import chemin_scenarios

def init_couleur_et_noms():
    init_cols = ['demande', 'electrolyse',
            'prodOffshore', 'prodOnshore', 'prodPV', 'rivprod', 'lakeprod',
            'Bprod', 'Bstored', 'Bcons',
            'Gprod', 'Gstored', 'Gcons',
            'Lprod', 'Lstored',
            'Nprod', 'Nstored',
            'Sprod', 'Sstored', 'Scons',
            'prodResiduelle', '-prodResiduelle',
            's', 'p',
            'résiduelNonPilotable'
            ]
    init_couls = ["black", "grey",
                "seagreen", "yellowgreen", "yellow", "aquamarine", "blue",
                "orange", "orange", "orange",
                "purple", "violet", "grey",
                "darkblue", "darkblue",
                "coral", "coral",
                "lightblue", "lightblue", "lightblue",
                "darkslategray", "darkslategray",
                "blue", "red",
                "grey"
                ]
    init_noms = [
        'demande (DM)', 'electrolyse',
        'prodOffshore', 'prodOnshore', 'prodPV', 'rivprod', 'lakeprod',
        'Batt', 'Bstored', 'Batt',
        'Gaz2power', 'Gaz stock', 'Power2Gaz',
        'Lprod', 'Lstored',
        'Nprod', 'Nstored',
        'Step', 'Stock Step', 'Step',
        'prodResiduelle', '-prodResiduelle',
        'surplus', "pénuries",
        'DM - non pilotable(NP)'
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

    def __init__(self, dm, annee, vue, data_mix="./data_mix/"):
        self.data_mix = data_mix
        self.dm = dm
        self.annee = annee
        self.vue = vue
        self.jinja_params = {
            "equipe": dm.equipe, 
            "partie": dm.partie,
            "annee": annee, 
            "vue": vue}
        
    def get_jinja_parameters(self):
        return self.jinja_params

    def genere_jinja_parameters(self):
        pass

class VisualiseurBokeh(Visualiseur):

    def __init__(self, dm, annee, vue, data_mix="./data_mix/"):
        super().__init__(dm, annee, vue, data_mix)
        self.figs = {}
        self.chroniques = dm.get_chroniques(annee)
        self.chroniques.apply(lambda col : col.repeat(2))
        dates = np.empty_like(self.chroniques["date"].values)
        dates[:-1] = self.chroniques["date"].values[1:]
        dates[-1] = self.chroniques["date"].values[-1]
        self.chroniques["date"] = dates
        self.chroniques = self.chroniques.reset_index()
        self.source = bk.models.ColumnDataSource(self.chroniques)

        self.dates = np.array(self.chroniques['date'], dtype=np.datetime64)

    def genere_jinja_parameters(self):
        self.set_figs()
        composants = self.get_composants()
        resources = INLINE.render()
        script = composants["script"]
        divs = composants["divs"]
        self.jinja_params.update({"bokeh_ressources": INLINE.render(),
                            "bokeh_script": script,
                            "bokeh_divs": divs
                            })


    def get_dates_et_source(self):
        return self.dates, self.source

    def set_fig(self, fig=bkp.figure(), titre="vierge"):
        self.figs[titre] = fig

    def set_figs(self):
        self.set_fig()

    def get_composants(self):
        script, divs = components(self.figs)
        return {"script": script, "divs": divs}

    def stack_plot(self, cols, fig=bkp.figure(x_axis_type="datetime"), méthode=None, pas_de_legende=False):
        if méthode is None:
            méthode = fig.varea_stack

        if pas_de_legende:
            méthode(stackers=cols, x="date", color=couleurs[cols].to_list(), source=self.source)

        else:
            
            méthode(stackers=cols, x="date", color=couleurs[cols].to_list(),
                        legend_label=noms[cols].to_list(), source=self.source)

        return fig

    def range_fig(self, deb=24 * 31, fin=24 * 31 + 24 * 14):
        p = bkp.figure(height=150, width=800, tools="xpan", toolbar_location=None,
                       x_axis_type="datetime", x_axis_location="below", sizing_mode="scale_width",
                       background_fill_color="#efefef", x_range=(self.dates[deb], self.dates[fin]))

        select = bkp.figure(title="Déplacez le milieu ou un bord du rectangle",
                            height=80, width=800, y_range=p.y_range, sizing_mode="scale_width",
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


class vScenario(VisualiseurBokeh):

    def set_fig_1(self):

        df = pd.read_hdf(chemin_scenarios + self.dm.partie + "_25-50.h5", "df")
        df.groupby(pd.Grouper( freq='5Y')).sum() 
        """ annee_en_cours = (self.annee.__str__())

        if int(annee_en_cours) >= 2050:
            df = df.loc["2050-1-1 0:0":"2050-12-31 23:0"]
        else:
            df = df.loc[annee_en_cours + "-1-1 0:0": annee_en_cours + "-12-31 23:0"]
        
        demande = df.groupby(df.date.dt.year)['demande'].sum() """

        return df
    def set_figs(self):
        self.set_fig_1()
        fig = self.stack_plot(cols=['demande', 'electrolyse'])
        self.set_fig(fig, "Scenario")


class vProduction(VisualiseurBokeh):


    def fig_prod(self):

        prods = ['rivprod',  'prodOffshore', "Nprod", "Lprod", 'prodOnshore', 'prodPV']
        self.chroniques['prods'] = self.chroniques[prods].sum(axis=1)
        self.chroniques['résiduel'] = self.chroniques["demande"] - self.chroniques["prods"]

        self.source = bk.models.ColumnDataSource(self.chroniques)

        p, select = self.range_fig()

        p.add_layout(bk.models.Legend(), 'right')
        p.legend.click_policy = "mute"
        p = self.stack_plot(cols=prods, fig=p)
        p.line(x='date', y='demande', source=self.source, line_width=2, color="black", legend_label=noms['demande'])
        p.yaxis.axis_label = 'productions hors stoc/destock et gaz (GW)'
        p.legend.click_policy = "mute"
        hover = bk.models.HoverTool(tooltips=[("Value", "@demande")])
        p.add_tools(hover)

        s = bkp.figure(height=150, width=800, tools=["box_zoom"], toolbar_location=None,
                       x_axis_type="datetime", x_axis_location="below", sizing_mode="scale_width",
                       background_fill_color="#efefef", x_range=p.x_range)

        s.add_layout(bk.models.Legend(), 'right')
        s.legend.click_policy = "mute"

        prod_stock = ["Bprod", "Sprod",  "Gprod", "p"]
        cons_stock = ["Bcons", "Scons",  "Gcons", "s"]
        s = self.stack_plot(cols=prod_stock, fig=s)
        s = self.stack_plot(cols=cons_stock, fig=s)
        s.line('date', 'résiduel', source=self.source, line_width=2, color="black",
               legend_label="demande restante")
        s.yaxis.axis_label = 'stock/déstock élec. + gaz. (GW)'
        s.legend.click_policy = "mute"

        stock = bkp.figure(height=150, width=800, tools=["box_zoom"], toolbar_location=None,
                       x_axis_type="datetime", x_axis_location="below", sizing_mode="scale_width",
                       background_fill_color="#efefef", x_range=p.x_range)
        stock = self.fig_stock(s=stock)
        select = self.stack_plot(cols=prods, fig=select, pas_de_legende=True)
        fig = column(select, p, s, stock, sizing_mode="scale_width")
        return fig

    def fig_stock(self, s = None):

        stock = ["Lstored", "Sstored", "Bstored", ]

        if s is None:
            s, select = self.range_fig()
            select = self.stack_plot(cols=stock, fig=select, pas_de_legende=True)
        else:
            select=None

        s.add_layout(bk.models.Legend(), 'right')
        s.legend.click_policy = "mute"

        s = self.stack_plot(cols=stock, fig=s)
        s.yaxis.axis_label = 'stocks (GWh)'
        s.legend.click_policy = "mute"

        if select is not None:
            return column(select, s, sizing_mode="scale_width")
        else:
            return s

    def fig_penuries(self):
        from bokeh.palettes import tol

        p, select = self.range_fig()

        cols = ["s", "p"]

        p = self.stack_plot(cols, p)
        p.line(x='date', y='demandeRésiduelle', source=self.source, legend_label='production résiduelle')
        p.yaxis.axis_label = 'surplus penuries (GW)'
        p.legend.click_policy = "mute"

        select.line('date', 'demandeRésiduelle', source=self.source)
        fig = column(p, select)
        return fig

        def fig_facteur_de_charge(self):
            pass

    def set_figs(self):
        self.set_fig(self.fig_prod(), "Pilotage de la production")


class vJournal(Visualiseur):
    def genere_jinja_parameters(self):

        datas = jr.calculer_data(self.dm, self.annee)

        self.jinja_params.update({"article": jr.exemple(datas)
                            })
   

vuesClasses = {"resultats": Visualiseur,
               "journal": vJournal,
               "scenario": vScenario,
               "production": vProduction
               }

if __name__ == "__main__":
    from flaskapp import archiveur
    import os
    chemin = os.path.dirname(os.path.realpath(__file__))
    dataPath = chemin + "/../flaskapp/"
    dm = archiveur.DataManager(equipe="winn", partie="S1", chemin=dataPath)

    chroniques = dm.get_chroniques("2025")
    resultats = dm.get_results()
    chroniques.describe()
    self = vProduction(chroniques)
    bkp.show(self.fig_prod())
#    self.set_figs()
#    composants = self.get_composants()
#    print(composants["divs"])
