import webapp2
import render
from models import MedKit, PostDefault, Supply, SupplyRequest
from forms import SupplyRequestForm
from google.appengine.ext import db
from datetime import datetime
import utilities


def simple_validate(v):
    medkit = db.get(v['mk'])
    if medkit == None:
        v['valid'] = False
    else:
        mk_post_code =  medkit.post_default.slug.lower()
        if v['kit_id'] != str(medkit.key().id()):
            v['valid'] = False
        elif mk_post_code != v['post_code'].lower():
            v['valid'] = False
        else:
            v['MedKit'] = db.get(v['mk'])
            v['volunteer'] = v['MedKit'].volunteer
            v['valid'] = True
    return v

class landing(webapp2.RequestHandler):
    def get(self, post_code=""):
        v = {'PostDefault': PostDefault}
        v['wrong_code'] = bool(self.request.get("wc"))
        if post_code == "":
            html = render.page(self, "templates/volunteer/landing.html", v)
            self.response.out.write(html)
        else:
            v['post_code'] = post_code.lower().replace("/", "")
            q = PostDefault.all().filter('slug =', v["post_code"])
            if q.count() > 0:
                html = render.page(self, "templates/volunteer/landing.html", v)
                self.response.out.write(html)
            else:
                render.not_found(self)


    def post(self):
        mk_code = self.request.POST['code']
        post_code = self.request.POST['post_code']
        medkit = MedKit.all().filter('code =', mk_code).get()
        if medkit != None:
            m_k = str(medkit.key())
            m_id = str(medkit.key().id())
            re_url = "/%s/%s/status?k=%s" % (post_code, m_id, m_k)
            self.redirect(re_url)
        else:
            self.redirect("/" + self.request.POST['post_code'] + "?wc=True")

class status(webapp2.RequestHandler):
    def get(self, post_code, kit_id):
        v = {}
        v['post_code'] = post_code
        v['kit_id'] = kit_id
        v['mk'] = self.request.get('k')
        v = simple_validate(v)
        if v['valid']:
            request_query = SupplyRequest.all().filter('medkit =', v["MedKit"]).order("-date")
            v['requests'] = utilities.sr_improver(request_query)
            html = render.page(self, "templates/volunteer/status_table.html", v)
            self.response.out.write(html)
        else:
            render.not_found(self)

class request_form(webapp2.RequestHandler):
    def get(self, post_code, kit_id):
        v = {}
        v['post_code'] = post_code
        v['kit_id'] = kit_id
        v['mk'] = self.request.get('k')
        v = simple_validate(v)
        if v['valid']:
            v['Supply'] = Supply
            v['srf'] = SupplyRequestForm()
            html = render.page(self, "templates/forms/supply_request.html", v)
            self.response.out.write(html)
        else:
            render.not_found(self)
    def post(self, post_code, kit_id):
        v = {'post_code': post_code,
             'kit_id': kit_id,
             'mk': self.request.get("mk")}
        v = simple_validate(v)
        if v['valid']:
            supplies = []
            quantities = []
            # PR AKA Post Reqest Dictionary
            PR = self.request.POST
            for post_item in PR:
                if post_item.split("_")[0] == 'supply':
                    supply = db.get(PR[post_item])
                    supplies.append(supply.key())
                    qty_find = "qty_" + post_item.split("_")[-1]
                    quantities.append(int(PR[qty_find]))
            new_sr = SupplyRequest(
                supplies = supplies,
                quantities = quantities,
                date = datetime.now(),
                delivery_event = None,
                status = "Requested",
                medkit = v["MedKit"],
                post_default = v["MedKit"].post_default
            )
            if PR['volunteer_notes'] != "":
                new_sr.volunteer_notes = PR['volunteer_notes']
            new_sr.put()
            redirect = "/%s/%s/status?k=%s" % (post_code, kit_id, v['mk'])
            self.redirect(redirect)
        else:
            self.response.write.out('something unexpected happened')
