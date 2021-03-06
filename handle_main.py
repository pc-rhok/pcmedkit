import webapp2
import home, superadmin, postadmin, volunteer
import render


app = webapp2.WSGIApplication([
                               (r'/(.+)/(\d+)',volunteer.status),
                               (r'/(.+)/(\d+)/request',volunteer.request_form),
                               (r'/(.+)/(\d+)/status',volunteer.status),
                               (r'/(.+)',volunteer.landing),
                               ('/',volunteer.landing),
                               ], debug=True)

siteadmin = webapp2.WSGIApplication([(r'/admin/(.+)/supplies', postadmin.supply_form),
                               (r'/admin/(.+)/requests', postadmin.requests_table),
                               (r'/admin/(.+)/update', postadmin.update),
                               (r'/admin/(.+)/assign_medkit', postadmin.medkit),
                               (r'/admin/(.+)', postadmin.requests_table),
                               (r'/admin', postadmin.landing),
                               ], debug=True)

superadmin = webapp2.WSGIApplication([(r'/admin/hq', superadmin.main),
                                      (r'/admin/hq/(.+)', superadmin.form),
                               ], debug=True)

not_found = webapp2.WSGIApplication([('/.*', render.not_found)], debug=True)