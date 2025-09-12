## OK ##
# config = {
#     'a': 1,
#     'b': 2,
#     'c': 3
# }

# def init(**conf):
#     for k,v in conf.items():
#         config[k] = v
        
#     print("Running with config:", config)
#     print("config.c:", config['c'])
#     print("config.d:", config['d'])

## ALSO OK ##
# cfg = dict(a=1, b=2, c=3)

# def init(**conf):
#     for k,v in conf.items():
#         cfg[k] = v
        
#     print("Running with config:", cfg)
#     print("config.c:", cfg['c'])
#     print("config.d:", cfg['d'])

# class Cfg:
#     a=1 
#     b=2 
#     c=3
#     d=4

#     def __init__(self, **kwargs):
#         for k,v in kwargs.items():
#             setattr(self, k, v)

#     def show(self):
#         print(locals().items())


# def init(**conf):
#     cfg = Cfg(**conf)
#     # cfg.show()
#     print(locals().items())
#     print(globals().items())

a = 1
b = 2
c = 3
d = 4

def init(**conf):
    for k,v in conf.items():
        globals()[k] = v

def show():
    print(a)
    print(b)
    print(c)



