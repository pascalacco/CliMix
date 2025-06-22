import bokeh as bk
import bokeh.plotting as bkp
from bokeh.embed import components
from bokeh.models import ColumnDataSource, RangeTool
from bokeh.layouts import column
from bokeh.io import curdoc
import numpy as np
import pandas as pd

from bokeh.resources import INLINE

from flask import json

import flaskapp.journal.journal as jr
import random

import os

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

    def __init__(self, dm, annee, vue):
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

    def __init__(self, dm, annee, vue):
        super().__init__(dm, annee, vue)
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

        if self.dm.partie == "2025Plat":
            df = self.dm.pays.get_scenario("S1")
        else:
            df = self.dm.pays.get_scenario(self.dm.partie)
            #df = pd.read_hdf(chemin_scenarios + self.dm.partie + "_25-50.h5", "df")

        df = df.groupby(pd.Grouper( freq='5Y')).sum()
        df["annee"] = [y.__str__() for y in df.index.year.values]
        cols = ['demande', 'electrolyse']
        #fig = bkp.figure(x_axis_type="datetime")
        fig = bkp.figure(x_range= df["annee"].values)
        fig.vbar_stack(stackers=cols, x="annee", color=couleurs[cols].to_list(),legend_label=noms[cols].to_list(), source=df)
        """ annee_en_cours = (self.annee.__str__())

        if int(annee_en_cours) >= 2050:
            df = df.loc["2050-1-1 0:0":"2050-12-31 23:0"]
        else:
            df = df.loc[annee_en_cours + "-1-1 0:0": annee_en_cours + "-12-31 23:0"]
        
        demande = df.groupby(df.date.dt.year)['demande'].sum() """

        return fig
    def set_figs(self):
        fig = self.set_fig_1()
        #fig = self.stack_plot(cols=['demande', 'electrolyse'])
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
        with open(f"{self.dm.chemin}/roles.json","r") as f:
            roles_dict = json.load(f)
        names = roles_dict["names"]
        pronouns = roles_dict["pronouns"]
        roles = roles_dict["roles"]

        datas = jr.calculer_data(self.dm, self.annee)

        infras_tour = [] #recup les infras sur lesquelles on a agi ce tour ci
        if datas.regions_photovoltaiques is not None:
            infras_tour.append("pv")
        if datas.regions_eolien_offshore is not None:
            infras_tour.append("off")
        if datas.regions_eolien_onshore is not None:
            infras_tour.append("on")
        if datas.regions_methaniseur is not None:
            infras_tour.append("meth")
        if datas.regions_suppression_nucleaire is not None:
            infras_tour.append("nuc suppr")
        if datas.regions_centrales_nucleaires is not None:
            infras_tour.append("nuc")
        if datas.regions_sous_production is not None:
            infras_tour.append("sous prod")

        num_written = 0 #on va faire des articles en fonction des rôles des joueurs et des actions du tour
        articles = []
        names_final = []
        roles_final = []
        picked_infra = []
        while num_written < 3:
            player = random.randint(0,len(roles)-1)
            role = roles[player]
            name = names[player]
            pronoun = pronouns[player]
            if role == "PDG solaire":
                if "pv" in infras_tour:
                    picked_infra.append("pv")
                    article, _ = jr.make_text(datas,name,pronoun,role)
                    articles.append(article)
                    num_written += 1
                    roles_final.append(role)
                    names_final.append(name)
                    roles.pop(player)
                    names.pop(player)
                    pronouns.pop(player)
            elif role == "PDG éolien":
                if "off" or "on" in infras_tour:
                    article, infra = jr.make_text(datas,name,pronoun,role)
                    if infra == "éolien onshore":
                        picked_infra.append("on")
                    else:
                        picked_infra.append("off")
                    articles.append(article)
                    num_written += 1
                    roles_final.append(role)
                    names_final.append(name)
                    roles.pop(player)
                    names.pop(player)
                    pronouns.pop(player)
            elif role == "agriculteur":
                if "pv" or "on" or "meth" in infras_tour:
                    article, infra = jr.make_text(datas,name,pronoun,role)
                    if infra == "photovoltaïque":
                        picked_infra.append("pv")
                    elif infra == "éolien onshore":
                        picked_infra.append("on")
                    else:
                        picked_infra.append("meth")
                    articles.append(article)
                    num_written += 1
                    roles_final.append(role)
                    names_final.append(name)
                    roles.pop(player)
                    names.pop(player)
                    pronouns.pop(player)
            elif role == "activiste":
                if "pv" or "off" or "on" or "meth" in infras_tour:
                    article, infra = jr.make_text(datas,name,pronoun,role)
                    if infra == "photovoltaïque":
                        picked_infra.append("pv")
                    elif infra == "éolien onshore":
                        picked_infra.append("on")
                    elif infra == "éolien offshore":
                        picked_infra.append("off")
                    else:
                        picked_infra.append("meth")
                    articles.append(article)
                    num_written += 1
                    roles_final.append(role)
                    names_final.append(name)
                    roles.pop(player)
                    names.pop(player)
                    pronouns.pop(player)
            elif role == "greenpeace":
                if "nuc" or "nuc suppr" in infras_tour:
                    article, infra = jr.make_text(datas,name,pronoun,role)
                    if infra == "maintenue":
                        picked_infra.append("nuc")
                    else:
                        picked_infra.append("nuc suppr")
                    articles.append(article)
                    num_written += 1
                    roles_final.append(role)
                    names_final.append(name)
                    roles.pop(player)
                    names.pop(player)
                    pronouns.pop(player)
            elif role == "élue":
                if "sous prod" or "nuc suppr" in infras_tour:
                    article, infra = jr.make_text(datas,name,pronoun,role)
                    if infra == "sous-production":
                        picked_infra.append("sous prod")
                    else:
                        picked_infra.append("nuc suppr")
                    articles.append(article)
                    num_written += 1
                    roles_final.append(role)
                    names_final.append(name)
                    roles.pop(player)
                    names.pop(player)
                    pronouns.pop(player)
            elif role == "première ministre":
                articles.append(jr.make_text(datas,name,pronoun,role))
                num_written += 1
                roles_final.append(role)
                names_final.append(name)
                roles.pop(player)
                names.pop(player)
                pronouns.pop(player)
        #get image infra 
        import os

        base_path = os.path.dirname(os.path.realpath(__file__)) + "/../flaskapp/static/images_une"
        infra = random.choice(picked_infra)
        if infra == "pv":
            list_imgs = [f for f in os.listdir(f"{base_path}/pv") if 'jpg' in f]
            infra_img = random.choice(list_imgs)
            infra_txt = infra_img.replace(".jpg",".txt")
            infra_img = f"/static/images_une/pv/{infra_img}"
            infra_txt = f"/static/images_une/pv/{infra_txt}"
        elif infra == "off":
            list_imgs = [f for f in os.listdir(f"{base_path}/offshore") if 'jpg' in f]
            infra_img = random.choice(list_imgs)
            infra_txt = infra_img.replace(".jpg",".txt")
            infra_img = f"/static/images_une/offshore/{infra_img}"
            infra_txt = f"/static/images_une/offshore/{infra_txt}"
        elif infra == "on":
            list_imgs = [f for f in os.listdir(f"{base_path}/onshore") if 'jpg' in f]
            infra_img = random.choice(list_imgs)
            infra_txt = infra_img.replace(".jpg",".txt")
            infra_img = f"/static/images_une/onshore/{infra_img}"
            infra_txt = f"/static/images_une/onshore/{infra_txt}"
        elif infra == "meth":
            list_imgs = [f for f in os.listdir(f"{base_path}/methaniseur") if 'jpg' in f]
            infra_img = random.choice(list_imgs)
            infra_txt = infra_img.replace(".jpg",".txt")
            infra_img = f"/static/images_une/methaniseur/{infra_img}"
            infra_txt = f"/static/images_une/methaniseur/{infra_txt}"
        elif infra == "nuc suppr":
            list_imgs = [f for f in os.listdir(f"{base_path}/demantelement") if 'jpg' in f]
            infra_img = random.choice(list_imgs)
            infra_txt = infra_img.replace(".jpg",".txt")
            infra_img = f"/static/images_une/demantelement/{infra_img}"
            infra_txt = f"/static/images_une/demantelement/{infra_txt}"
        elif infra == "nuc":
            list_imgs = [f for f in os.listdir(f"{base_path}/nucleaire") if 'jpg' in f]
            infra_img = random.choice(list_imgs)
            infra_txt = infra_img.replace(".jpg",".txt")
            infra_img = f"/static/images_une/nucleaire/{infra_img}"
            infra_txt = f"/static/images_une/nucleaire/{infra_txt}"
        elif infra == "sous prod":
            list_imgs = [f for f in os.listdir(f"{base_path}/sousproduction") if 'jpg' in f]
            infra_img = random.choice(list_imgs)
            infra_txt = infra_img.replace(".jpg",".txt")
            infra_img = f"/static/images_une/sousproduction/{infra_img}"
            infra_txt = f"/static/images_une/sousproduction/{infra_txt}"
        
        #get image greenwashing
        list_imgs = [f for f in os.listdir(f"{base_path}/greenwashing") if 'jpg' in f]
        greenwashing_img = random.choice(list_imgs)
        greenwashing_txt = greenwashing_img.replace(".jpg",".txt")
        greenwashing_img = f"/static/images_une/greenwashing/{greenwashing_img}"
        greenwashing_txt = f"/static/images_une/greenwashing/{greenwashing_txt}"

        self.jinja_params.update({"articles": articles,"names":names_final,"roles":roles_final,"infra_img":infra_img,"infra_txt":infra_txt,"greenwashing_img":greenwashing_img,"greenwashing_txt":greenwashing_txt})

class vResults(Visualiseur):
    def genere_jinja_parameters(self):

        resultats = self.dm.get_results()

        self.jinja_params.update(
            {"resultats": json.dumps(resultats)}
        )

vuesClasses = {"resultats": vResults,
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
