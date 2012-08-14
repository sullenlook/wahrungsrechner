#!/usr/bin/python
# -*- coding: utf-8 -*-
# Convertisseur de monnaie
# Par Cédric Boverie (cedbv)

import re
import urllib2, urllib
from plugin import *

class currencyConverter(Plugin):

    def str2CurrencyCode(self, string):
        if string == "euros" or string == "euro":
            return "EUR"
        elif string == "dollar" or string == "dollars":
            return "USD"
        else:
            return ""

    @register("de-DE", ".*Tausche (?P<amount>[0-9,\.]+) (?P<from>[^ ]+) in (?P<to>[^ ]+)")
    def converter(self, speech, language, regMatched):

        amount = regMatched.group("amount").strip()
        currency_from = regMatched.group("from").strip()
        currency_to = regMatched.group("to").strip()

        currency_from_code = self.str2CurrencyCode(currency_from)
        currency_to_code = self.str2CurrencyCode(currency_to)

        if currency_from_code == currency_to_code:
            self.say(u"Kommen schon, du weisst, die Berechnung selbst...")
            self.complete_request()
            return
        elif currency_from_code == "" or currency_to_code == "":
            self.say(u"Ich habe nicht alle benoetigten Muenzen gefunden...")
            self.complete_request()
            return

        try:
            amount = amount.replace(",",".").replace(" ","")
            amount = float(amount)
        except:
            self.say(u"Ich kann den gesuchten Wert nicht interpretieren.")
            self.complete_request()
            return


        self.say(u"Ich rechne "+str(amount)+" "+currency_from+" in "+currency_to+" um...")

        change = None
        try:
            change = urllib2.urlopen("http://quote.yahoo.com/d/quotes.csv?s={0}{1}=X&f=l1&e=.csv".format(currency_from_code,currency_to_code), timeout=5).read()
        except:
            pass

        if change != None:
            self.say(str(amount) + " " + currency_from + u" sind etwa " +str(round(amount*float(change),2))+ " "+currency_to + ".")
        else:
            self.say(u"Ich schaffe es nicht den aktuellen Wechselkurs zu finden.")

        self.complete_request()