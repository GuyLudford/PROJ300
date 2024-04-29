from roboflow import Roboflow
rf = Roboflow(api_key="t7NQ4lrREZgkEIridF8Z")
project = rf.workspace("blackcreed-xpgxh").project("climbing-holds-and-volumes")
version = project.version(7)
dataset = version.download("yolov7")
