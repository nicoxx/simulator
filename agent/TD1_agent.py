'''
Created on Feb 17, 2014

@author: V Grosbois - N Lecrique
'''

from objects.Order import *

from datetime import datetime


def pretty(d, indent=0):
   for key, value in d.iteritems():
      print '\t' * indent + str(key)
      if isinstance(value, dict):
         pretty(value, indent+1)
      else:
         print '\t' * (indent+1) + str(value)
         
         
class TD1_agent():
    def __init__(self, service_locator, params):
        self.services = service_locator
        self.parameters = params
        if not self.parameters.has_key("id"):
            self.parameters["id"] = "TD1_agent"
    
    def process(self, symbol):        
        data = self.services.bus.get_market_data()        
        
        
        pretty(data) #display market data
        
        l = list()
         
        for item1 in data.items():
            if type(item1[1]) is not datetime and type(item1[1]) is not str:
                for item2 in item1[1].items():
                    if (item2[0][:3] == 'ask' and str(self.parameters["side"]).lower() == "buy") or (item2[0][:3] == 'bid' and str(self.parameters["side"]).lower() == "sell") :
                        l.append((item2[1]["price"], item1[0]))
         
        
        if str(self.parameters["side"]).lower() == "buy":
            l.sort(key=lambda x: x[0])
        else:
            l.sort(key=lambda x: -x[0])
        
        print(l)    #display list of prices by market ordered by prices
        
        self.current_size  = self.parameters["size"]
              
        i = 0
        for pair in l:  
            if self.current_size == 0:  #stop if no more deals
                break
            
            
            o = Order()
            o.side = 1 if str(self.parameters["side"]).lower() == "buy" else -1
            o.price = pair[0]
            
        
            #dont buy / sell if the price is too high or too low
            if o.price < self.parameters["price"] and o.side == -1:
                break
            if o.price > self.parameters["price"] and o.side == 1:
                break
                       
            o.size = self.current_size
            o.leaves = o.size
            o.symbol = pair[1]
            o.id = "MyOrder_" + str(i)
            o.timeinforce = "ioc"
            o.parent = self.parameters["id"]
            
            self.services.logger.info("Sending Order " + str(i))
            self.services.order_dispatcher.new_order(o)
            i = i +1
            
            
    def process_report(self, id):
        execs = self.services.bus.get_executions()[id]
        
        self.services.logger.info("----> execution!!" + str(id)  + " number: " +  str(len(execs)))
        for e in execs:
            self.services.logger.info(e)
            self.current_size -= e.size
            #change current quantity when an execution has been made

            
            
    def process_reject(self, order_id):
        reject = self.services.bus.get_rejects()[order_id]  
        if reject.leaves > 0 :
            self.services.logger.info("reject: %s. RemainingQty: %d" % (order_id, reject.leaves))