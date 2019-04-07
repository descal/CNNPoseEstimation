
import converter
import banana



converter.main("data/ModelNet10/monitor/test/monitor_0466.off","data/test.obj","obj",None,None)


banana.peel(10,0.5) # (Number of viewpoints, Distance from model)
banana.look() # Visualize model


