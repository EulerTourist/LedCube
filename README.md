# Names of cube_tfmcube faces:
#           ^
#           D
#           |                   Panel:
#           B                   0,0 1,0 -> W,0
#           v                   0,1 ---->   |
#           ^                    | ---->    |
#  L> ----- U ----- <R           | --->     |
#           |                   0,H ->     W,H
#           ^
#           F
# 
# Snake: 
# red head=1, body of alternate greens
# new snake starts on random pixel and random direction (U,D,L,R), start one straight away then every rand()*10sec 
# each snake moves by one pixel each step, L=-1, R=+1, U=-W, D=+W in the current direction, update all pixels
# however, preceding the step, snake may change direction turning left or right with a probablity of P=1/(4*(H+W)) 
# if the snake reaches the edge of the panel, go adjacent panel
# snake starts with body=0 and extends by one each time it crosses an edge, that is, not deleting last
# snake fades out when length attempts to increment to max length N=2*(H+W), that is, at edge
# Specs:
# px = (0pxy, 0rgb)
# snake = { dir: <U/D/L/R/Fade>, bright:<byte>, px: deque}
# NB: calculate as RGB but GRB on the pixel
