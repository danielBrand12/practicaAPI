from tortoise.contrib.pydantic import pydantic_model_creator
from app.models.models import customer, timeinterval, cust_order2, material, lineitem, plant, storagelocation, stock, demand


customer_pydantic = pydantic_model_creator(customer, name="Customer")
customerIn_pydantic = pydantic_model_creator(customer, name="CustomerIn", exclude_readonly=True)
cust_order2_pydantic = pydantic_model_creator(cust_order2, name="Cust_Order")
timeinterval_pydantic = pydantic_model_creator(timeinterval, name="Time_Interval")
material_pydantic = pydantic_model_creator(material, name="Material")
materialIn_pydantic = pydantic_model_creator(material, name="MaterialIn", exclude_readonly=True)
lineitem_pydantic = pydantic_model_creator(lineitem, name="Line_Item")
plant_pydantic = pydantic_model_creator(plant, name="Plant")
plantIn_pydantic = pydantic_model_creator(plant, name="PlantIn", exclude_readonly=True)
storagelocation_pydantic = pydantic_model_creator(storagelocation, name="Storage_Location")
storagelocationIn_pydantic = pydantic_model_creator(storagelocation, name="Storage_LocationIn", exclude_readonly=True)
stock_pydantic = pydantic_model_creator(stock, name="Stock")
demand_pydantic = pydantic_model_creator(demand, name="Demand")