import bokeh as bk
import bokeh.plotting as bkp
from bokeh.embed import components



class Visualiseur:
    def __init__(self, chroniques):
        self.fig = bkp.figure()
        self.chroniques = chroniques
        self.source = bk.models.ColumnDataSource(chroniques)
    def get_fig(self):
        return self.fig

    def set_fig(self):
        return self.fig

    def get_composants(self, vue):
        script, div = components(self.fig)
        return {"script": script, "div": div}

    def cumul_plot(self, cols, palette=bk.palettes.Category10_10):
        couleurs = iter(palette)
        self.fig.varea_stack(stackers=cols, x="heures", color=[next(couleurs) for col in cols], legend_label=cols, source=self.source )


class vScenario(Visualiseur):
    def set_fig(self):
        palette = bk.palettes.Category10_10
        couleurs = iter(palette)
        self.cumul_plot(cols=['demande', 'electrolyse'])


vuesClasses = {"general": Visualiseur, "production": vScenario}