import bokeh as bk
import bokeh.plotting as bkp
from bokeh.embed import components

import pandas as pd


class Visualiseur:
    def __init__(self, chroniques, data_mix="./data_mix/"):
        self.data_mix = data_mix
        self.figs = []
        self.chroniques = chroniques
        self.source = bk.models.ColumnDataSource(chroniques)

    def set_fig(self, fig=bkp.figure()):
        self.figs.append(fig)

    def set_figs(self):
        self.set_fig()

    def get_composants(self, vue):
        script, divs = components(self.figs)
        return {"script": script, "divs": divs}

    def cumul_plot(self, cols, palette=bk.palettes.Category10_10):
        couleurs = iter(palette)
        fig = bkp.figure(x_axis_type="datetime")
        fig.varea_stack(stackers=cols, x="date", color=[next(couleurs) for col in cols], legend_label=cols, source=self.source )
        fig.legend.click_policy = "mute"
        self.set_fig(fig)

class vScenario(Visualiseur):

    def set_fig_1(self):
        fich = "S1_25-50.csv"
        df = pd.read_csv(self.data_mix + fich)

    def set_figs(self):
        palette = bk.palettes.Category10_10
        couleurs = iter(palette)
        self.cumul_plot(cols=['demande', 'electrolyse'])


vuesClasses = {"resultats": Visualiseur, "scenario": vScenario}