import bokeh as bk
import bokeh.plotting as bkp
from bokeh.embed import components
from bokeh.models import ColumnDataSource, RangeTool
from bokeh.layouts import column
from bokeh.io import curdoc
import numpy as np
import pandas as pd


class Visualiseur:
    def __init__(self, chroniques, data_mix="./data_mix/"):
        self.data_mix = data_mix
        self.figs = {}
        chroniques['prod_stock'] = chroniques[["Gprod", "Bprod", "Pprod", "Lprod"]].sum(axis=1)
        chroniques['-prodResiduelle'] = -chroniques["prodResiduelle"]
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

    def cumul_plot(self, cols, palette=bk.palettes.Category10_10):
        couleurs = iter(palette)
        fig = bkp.figure(x_axis_type="datetime")
        fig.varea_stack(stackers=cols, x="date", color=[next(couleurs) for col in cols], legend_label=cols, source=self.source )
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


class vScenario(Visualiseur):

    def set_fig_1(self):
        fich = "S1_25-50.csv"
        df = pd.read_csv(self.data_mix + fich)

    def set_figs(self):
        palette = bk.palettes.Category10_10
        couleurs = iter(palette)
        fig = self.cumul_plot(cols=['demande', 'electrolyse'])
        self.set_fig(fig, "Scenario")

class vProduction(Visualiseur):

    def fig_prod(self):
        from bokeh.palettes import tol

        p, select = self.range_fig()

        colonnes = self.chroniques.columns.values
        prod = [col for col in colonnes if
                ("prod" in col) and ("prodResiduelle" not in col) and ("prod_stock" not in col)]
        # p.line('date', 'prodResiduelle', source=source)
        p.varea_stack(stackers=prod, x='date', color=tol['Bright'][6][:len(prod)], legend_label=prod, source=self.source)
        p.line(x='date', y='-prodResiduelle', source=self.source, legend_label='production résiduelle')
        p.yaxis.axis_label = 'production (GW)'
        p.legend.click_policy = "mute"

        select.line('date', '-prodResiduelle', source=self.source)
        fig = column(p, select)
        return fig

    def fig_penuries(self):
        from bokeh.palettes import tol

        p, select = self.range_fig()

        colonnes = ["s", "p"]

        p.varea_stack(stackers=colonnes, x='date', color=tol['Bright'][6][:len(colonnes)], legend_label=colonnes, source=self.source)
        p.line(x='date', y='-prodResiduelle', source=self.source, legend_label='production résiduelle')
        p.yaxis.axis_label = 'surplus penuries (GW)'
        p.legend.click_policy = "mute"

        select.line('date', '-prodResiduelle', source=self.source)
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
    import archiveur

    dm = archiveur.DataManager(equipe="IMACS_A1", partie="S1")
    chroniques = dm.get_chroniques()
    resultats = dm.get_results()
    chroniques.describe()
    self = vProduction(chroniques)
    #bkp.show(self.fig_prod())
    self.set_figs()
    composants = self.get_composants()
    print(composants["divs"])

