from MSE.step1 import xml_to_table
from MSE.step2 import projections_to_behavior, table_to_projections
from MSE.step3 import get_io_from_behavior, write_to_uml, xml_to_table
from MSE.models import *


xml_file = "hi.xml"


table = xml_to_table(xml_file)

print(table)


projections = table_to_projections(table)

print(projections)

behavior = projections_to_behavior(projections)

print(behavior)

io_automaton = get_io_from_behavior(behavior)

print(io_automaton)

write_to_uml(io_automaton)
